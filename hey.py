import streamlit as st
import pandas as pd

def main():
    # Set page configuration
    st.set_page_config(
        page_title="DPDP Assessment Tool",
        page_icon="🔒",
        layout="wide"
    )
    
    # Application header
    st.title("Data Protection & Digital Privacy Assessment Tool")
    st.markdown("Evaluate your organization's DPDP compliance and get personalized recommendations.")
    
    # Sidebar navigation (removed the typo "o render")
    page = st.sidebar.radio("Navigation", ["Home", "Assessment", "Recommendations", "Resources", "About Us"])
    
    if page == "Home":
        show_home_page()
    elif page == "Assessment":
        show_assessment_page()
    elif page == "Recommendations":
        show_recommendations_page()
    elif page == "Resources":
        show_resources_page()
    elif page == "About Us":
        show_about_page()

# Add this new function at the end of the file, before if __name__ == "__main__":
def show_about_page():
    st.header("About Us")
    st.markdown("### Welcome to our Team!")
    
    # Read and encode the GIF file
    import base64
    from pathlib import Path
    
    def load_gif(gif_path):
        with open(gif_path, "rb") as file:
            return base64.b64encode(file.read()).decode()
    
    gif_path = "d:/sushma kulkarni/assessment/rahul.gif"
    encoded_gif = load_gif(gif_path)
    
    # Display the GIF using HTML with proper encoding
    st.markdown(f"""
        <div style='text-align: center; padding: 20px;'>
            <img src="data:image/gif;base64,{encoded_gif}" style='max-width: 80%; border-radius: 10px;'>
        </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    We are dedicated to helping organizations improve their data protection and privacy practices.
    Our assessment tool provides personalized recommendations to enhance your compliance journey.
    """)

def show_home_page():
    st.header("Welcome to the DPDP Assessment Tool")
    
    st.markdown("""
    This tool helps you evaluate your organization's compliance with data protection and privacy requirements.
    
    ### How it works:
    1. Complete the assessment questionnaire
    2. Get tailored recommendations based on your responses
    3. Access resources to improve your data protection practices
    
    Click on "Assessment" in the sidebar to begin.
    """)
    
    col1, col2 = st.columns(2)
    with col1:
        st.info("📋 The assessment takes approximately 5 minutes to complete.")
    with col2:
        st.info("🔒 Your data isn't stored or shared - this tool runs entirely in your browser.")

def show_assessment_page():
    st.header("DPDP Assessment Questionnaire")
    
    # Initialize session state for storing responses if not already present
    if 'responses' not in st.session_state:
        st.session_state.responses = {}
    
    # Define assessment sections and questions - SIMPLIFIED TO 2 SECTIONS WITH 2-3 QUESTIONS EACH
    sections = {
        "Data Collection & Storage": [
            {"id": "dc1", "question": "Does your organization collect personal data?", 
             "options": ["Yes", "No", "Not sure"]},
            {"id": "dc2", "question": "Do you have a privacy policy that explains data collection practices?", 
             "options": ["Yes", "No", "In development"]},
            {"id": "ds1", "question": "Is collected personal data encrypted?", 
             "options": ["Yes", "No", "Partially", "Not sure"]}
        ],
        "User Rights & Compliance": [
            {"id": "ur1", "question": "Can users request access to their personal data?", 
             "options": ["Yes - automated process", "Yes - manual process", "No"]},
            {"id": "ur2", "question": "Can users request deletion of their personal data?", 
             "options": ["Yes - automated process", "Yes - manual process", "No"]}
        ]
    }
    
    # Create form for assessment
    with st.form("assessment_form"):
        for section, questions in sections.items():
            st.subheader(section)
            for q in questions:
                response = st.radio(q["question"], q["options"], key=q["id"])
                # Store response in session state
                st.session_state.responses[q["id"]] = response
            st.divider()
        
        # Submit button
        submitted = st.form_submit_button("Submit Assessment")
        if submitted:
            st.success("Assessment completed! Please navigate to the Recommendations page.")

def show_recommendations_page():
    st.header("Your DPDP Recommendations")
    
    if not st.session_state.get('responses'):
        st.warning("Please complete the assessment first to get personalized recommendations.")
        if st.button("Go to Assessment"):
            st.session_state.page = "Assessment"
            st.experimental_rerun()
        return
    
    # Generate score
    score = generate_score(st.session_state.responses)
    
    # Display score
    st.subheader(f"Your DPDP Compliance Score: {score}%")
    
    col1, col2 = st.columns([1, 2])
    with col1:
        display_score_gauge(score)
    with col2:
        if score >= 80:
            st.success("Your organization demonstrates strong DPDP practices!")
        elif score >= 60:
            st.info("Your organization has decent DPDP practices but there's room for improvement.")
        else:
            st.error("Your organization needs significant improvements in DPDP practices.")
    
    # Generate and display recommendations
    recommendations = generate_recommendations(st.session_state.responses)
    
    st.subheader("Personalized Recommendations")
    for category, items in recommendations.items():
        with st.expander(f"{category} ({len(items)} recommendations)"):
            for item in items:
                st.markdown(f"- **{item['title']}**: {item['description']}")
                if 'action' in item:
                    st.info(f"**Suggested action**: {item['action']}")
    
    # Option to download recommendations
    if st.button("Download Recommendations as PDF"):
        st.info("This feature would generate a PDF report of recommendations.")

def show_resources_page():
    st.header("DPDP Resources")
    
    resources = [
        {
            "title": "DPDP Compliance Guide",
            "description": "A comprehensive guide to understanding data protection requirements",
            "type": "Guide",
            "link": "#"
        },
        {
            "title": "Privacy Policy Template",
            "description": "Customizable template for creating a compliant privacy policy",
            "type": "Template",
            "link": "#"
        },
        {
            "title": "Data Breach Response Plan",
            "description": "Step-by-step process for handling data breaches",
            "type": "Template",
            "link": "#"
        }
    ]
    
    # Display resources in a nice table
    df = pd.DataFrame(resources)
    st.dataframe(df, use_container_width=True, hide_index=True)

def generate_score(responses):
    # Simplified scoring system for the reduced question set
    weights = {
        "dc1": 5, "dc2": 8, "ds1": 10,
        "ur1": 9, "ur2": 9
    }
    
    # Define scoring for each possible answer
    scoring = {
        "dc1": {"Yes": 0.5, "No": 1.0, "Not sure": 0.3},
        "dc2": {"Yes": 1.0, "No": 0.0, "In development": 0.5},
        "ds1": {"Yes": 1.0, "No": 0.0, "Partially": 0.6, "Not sure": 0.3},
        "ur1": {"Yes - automated process": 1.0, "Yes - manual process": 0.7, "No": 0.0},
        "ur2": {"Yes - automated process": 1.0, "Yes - manual process": 0.7, "No": 0.0}
    }
    
    total_weight = sum(weights.values())
    weighted_score = 0
    
    for q_id, response in responses.items():
        if q_id in weights and q_id in scoring and response in scoring[q_id]:
            weighted_score += weights[q_id] * scoring[q_id][response]
    
    # Calculate percentage score
    percentage = (weighted_score / total_weight) * 100
    return round(percentage)

def display_score_gauge(score):
    # Create a simple score visualization
    import matplotlib.pyplot as plt
    import numpy as np
    
    fig, ax = plt.subplots(figsize=(3, 3))
    ax.add_patch(plt.Circle((0.5, 0.5), 0.4, color='lightgray'))
    ax.add_patch(plt.Circle((0.5, 0.5), 0.3, color='white'))
    
    # Add colored arc based on score
    theta = np.linspace(np.pi, np.pi * (1 - score/100) + np.pi, 100)
    x = 0.5 + 0.35 * np.cos(theta)
    y = 0.5 + 0.35 * np.sin(theta)
    
    if score >= 80:
        color = 'green'
    elif score >= 60:
        color = 'orange'
    else:
        color = 'red'
    
    ax.fill_between(x, y, 0.5, color=color, alpha=0.8)
    
    ax.text(0.5, 0.5, f"{score}%", ha='center', va='center', fontsize=20)
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.axis('off')
    
    st.pyplot(fig)

def generate_recommendations(responses):
    # Simplified recommendations for the reduced question set
    recommendations = {
        "Data Collection & Storage": [],
        "User Rights": [],
        "Documentation": []
    }
    
    # Example recommendation generation logic
    if responses.get("dc2") == "No":
        recommendations["Documentation"].append({
            "title": "Create Privacy Policy",
            "description": "Your organization needs a privacy policy that clearly explains data collection and processing practices.",
            "action": "Develop and publish a privacy policy on your website and other points of data collection."
        })
    
    if responses.get("ds1") in ["No", "Partially"]:
        recommendations["Data Collection & Storage"].append({
            "title": "Enhance Data Encryption",
            "description": "Personal data should be encrypted both in transit and at rest.",
            "action": "Implement end-to-end encryption for all personal data."
        })
    
    if responses.get("ur1") == "No":
        recommendations["User Rights"].append({
            "title": "Data Access Requests",
            "description": "Users have the right to access their personal data.",
            "action": "Implement a process for handling data subject access requests."
        })
    
    if responses.get("ur2") == "No":
        recommendations["User Rights"].append({
            "title": "Right to Erasure",
            "description": "Users have the right to request deletion of their personal data.",
            "action": "Implement a process for handling data deletion requests."
        })
    
    # Add some default recommendations if categories are empty
    for category in recommendations:
        if not recommendations[category]:
            recommendations[category].append({
                "title": f"Review {category} Practices",
                "description": "Regular review of practices in this area is recommended even if current compliance is good.",
                "action": f"Schedule quarterly reviews of {category.lower()} practices and documentation."
            })
    
    return recommendations

if __name__ == "__main__":
    main()