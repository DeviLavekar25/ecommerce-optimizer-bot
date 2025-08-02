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
    
    ''' results={}

    def parse_output(text, key):
        lines=[line.strip() for line in text.split('\n') if '|' in line]
        for line in lines:
            try:
                product_name,recommendation = line.split('|',1)
                product_name=product_name.strip().replace('-','').replace('*','').strip()
                recommendation=recommendation.strip()

                if product_name not in results:
                    results[product_name]={'audit':[],'pricing':[],'seo':[]}

                results[product_name][key].append(recommendation)
            except ValueError:
                continue
    
    audit_section = output_text.split("Final Answer for Task: Product Auditor")[1].split("Final Answer for Task: Pricing Optimizer")[0] if "Final Answer for Task: Product Auditor" in output_text else ""
    pricing_section = output_text.split("Final Answer for Task: Pricing Optimizer")[1].split("Final Answer for Task: SEO Expert")[0] if "Final Answer for Task: Pricing Optimizer" in output_text else ""
    seo_section = output_text.split("Final Answer for Task: SEO Expert")[1] if "Final Answer for Task: SEO Expert" in output_text else ""

    parse_output(audit_section,'audit')
    parse_output(pricing_section, 'pricing')                                                                            
    parse_output(seo_section, 'seo')                                              
                                            


    # Construct the final HTML output
    html_output = f"""
        <div style="background-color: #1e1e1e; padding: 20px; border-radius: 10px;">
            <h2 style="color: #FFD700;">📄 E-Commerce Optimization Report</h2>
    """

    for product, data in results.items():
        if not any (data.values()):
            continue

        html_output += f"""
            <div style="margin-top: 20px;">
                <h3 style="color: #1abc9c;">🛍️ {product}</h3>
                <h4 style="color: #ff69b4;">🔍 Product Audit:</h4>
                <ul>
        """
        for point in data['audit']:
            html_output += f"<li style='color: white;'>{point}</li>"
        if not data['audit']:
            html_output += "<li style='color: gray;'>No audit recommendations available.</li>"

        html_output += "</ul><h4 style='color: #ff8c00;'>💰 Pricing Optimization:</h4><ul>"
        for point in data['pricing']:
            html_output += f"<li style='color: white;'>{point}</li>"
        if not data['pricing']:
            html_output += "<li style='color: gray;'>No pricing recommendations available.</li>"

        html_output += "</ul><h4 style='color: #7fff00;'>📈 SEO Improvements:</h4><ul>"
        for point in data['seo']:
            html_output += f"<li style='color: white;'>{point}</li>"
        if not data['seo']:
            html_output += "<li style='color: gray;'>No SEO recommendations available.</li>"

        html_output += "</ul><hr style='border: 1px solid #444444;'></div>"

    html_output += "</div>"

    if results:
    
    # Use st.markdown to display the final HTML in Streamlit
        st.markdown(html_output, unsafe_allow_html=True)
    else:
        st.warning("No striuctured output could be parsed from the agent responses")

    with st.expander("Show raw Crew Output for Debugging"):
        st.markdown(f"<pre>{output_text}</pre>",unsafe_allow_html=True)


'''