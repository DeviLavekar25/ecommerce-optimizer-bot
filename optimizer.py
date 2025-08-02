import os
from crewai import Agent, Task, Crew
import streamlit as st
from dotenv import load_dotenv

load_dotenv()

# Agents
product_auditor = Agent(
    role='Product Auditor',
    goal='Audit the product listings on an e-commerce site',
    backstory='Expert in product analysis, reviews, and image quality.',
    verbose=True
)

pricing_optimizer = Agent(
    role='Pricing Optimizer',
    goal='Analyze pricing and suggest improvements to increase sales',
    backstory='Specialist in competitive pricing and sales psychology.',
    verbose=True
)

seo_expert = Agent(
    role='SEO Expert',
    goal='Improve SEO of product listings by optimizing titles and descriptions',
    backstory='Knows SEO best practices for online marketplaces.',
    verbose=True
)

report_writer = Agent(
    role='Report Writer',
    goal='Create a single, comprehensive report that consolidates the findings of all 3 agents and categorizes them by product.',
    backstory='You are a master of data synthesis and report generation. Your mission is to take the raw outputs from the Product Auditor, Pricing Optimizer, and SEO Expert and format them into a single, easy-to-read document. The report must be structured with clear headings for each product, followed by sections for each agent findings.',
    verbose=True
)

def get_tasks(site_url):
    audit_task = Task(
        description=f'Audit all product listings on {site_url} and highlight poor-quality images or negative reviews.',
        expected_output='List of issues found in products with reasons.',
        agent=product_auditor
    )

    pricing_task = Task(
        description=f'Analyze current product prices on {site_url} and suggest new ones to improve conversion rates.',
        expected_output='Recommended prices for each product with justification.',
        agent=pricing_optimizer
    )

    seo_task = Task(
        description=f'Evaluate and improve SEO in product titles and descriptions on {site_url}.',
        expected_output='Rewritten SEO-optimized titles and descriptions.',
        agent=seo_expert
    )

    consolidate_task= Task(
        description=f'Combine the outputs from the Product Auditor, Pricing Optimizer, and SEO Expert into a single, well structured report for the products on {site_url}. For each product create a main heading and then list the audit, pricing and seo recommendations'
        "\n\nHere is the required structure for the final output:"
        "\n\n### 1. Product: [Product Name]"
        "\n- **🔍 Product Audit:**"
        "\n  - [List of audit findings]"
        "\n- **💰 Pricing Recommendations:**"
        "\n  - [List of pricing suggestions]"
        "\n- **📈 SEO Improvements:**"
        "\n  - [List of SEO suggestions]"
        "\n\n### 2. Product: [Second Product Name]"
        "\n..."
        "\n\nEnsure that all data from the other agents is included and presented in this exact format. If an agent "
        "did not provide a recommendation for a specific product, state 'No recommendations available.' under that subheading.",
        expected_output='A detailed, markdown-formatted report that consolidates all agent findings, and categorized by product with clear headings for Product Audit, Pricing recommendations and SEO improvements.',
        agent=report_writer,
        context=[audit_task, pricing_task, seo_task]
    )

    return [audit_task, pricing_task, seo_task, consolidate_task]

def run_optimizer(site_url):
    tasks = get_tasks(site_url)
    crew = Crew(
      agents=[product_auditor, pricing_optimizer, seo_expert, report_writer],
       tasks=tasks,
       verbose=True
      )

    try:
      crew_output = crew.kickoff()
      output_text=str(crew_output)

      st.markdown("### Final Optimization Report 📄")
      st.markdown(output_text, unsafe_allow_html=True)

    except Exception as e:
      st.error(f'An error occurred:{e}')
      return
    
   