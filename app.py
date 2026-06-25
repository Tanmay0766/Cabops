import json
import streamlit as st
from LLM import analyze
from prompt import SYSTEM_PROMPT
from business_logic import calculate_incident_metrics


st.set_page_config(
    page_title="CabOps AI",
    layout="wide"
)

st.title("CabOps AI")
st.caption("Smart Incident Management System")


#INCIDENT INPUT
st.header("Incident Details")

col1, col2 = st.columns(2)

with col1:

    driver = st.text_input("Driver Marked Absent")

    route = st.text_input("Route")

    client = st.text_input("Client")

    picked = st.number_input(
        "Employees Picked",
        min_value=0,
        value=3
    )

with col2:

    waiting = st.number_input(
        "Employees Waiting",
        min_value=0,
        value=4
    )

    backup_capacity = st.number_input(
        "Backup Vehicle Capacity",
        min_value=1,
        value=4
    )

    weather = st.selectbox(
        "Weather",
        [
            "Clear",
            "Rain",
            "Heavy Rain"
        ]
    )

breakdown = st.text_area(
    "Vehicle Breakdown"
)

client_message = st.text_area(
    "Client HR Message"
)

# BUTTON
if st.button("Analyze Incident", use_container_width=True):

    incident = {

        "driver_absent": driver,

        "route": route,

        "client": client,

        "employees_picked": picked,

        "employees_waiting": waiting,

        "backup_capacity": backup_capacity,

        "vehicle_breakdown": breakdown,

        "weather": weather,

        "client_hr_message": client_message

    }

    metrics = calculate_incident_metrics(
        incident
    )

    with st.spinner("Analyzing..."):

        try:

            response = analyze(
                incident,
                metrics,
                SYSTEM_PROMPT
            )

        except Exception as exc:

            st.error("AI analysis is currently unavailable.")
            st.info("Please wait for the Gemini quota to reset, then try again.")
            st.caption(str(exc))
            st.stop()

    response = response.replace("```json", "")
    response = response.replace("```", "")
    response = response.strip()

    try:

        result = json.loads(response)

    except Exception:

        st.error("Gemini returned invalid JSON")

        st.code(response)

        st.stop()


    # SUMMARY
    st.success("Analysis Complete")

    st.divider()

    c1, c2, c3 = st.columns(3)

    c1.metric(
        "Priority",
        result["priority"]["level"]
    )

    c2.metric(
        "Affected Employees",
        metrics["affected_employees"]
    )

    c3.metric(
        "Risk Score",
        metrics["risk_score"]
    )

    st.divider()


    # PRIORITY
    st.subheader("Priority")

    st.write(result["priority"]["summary"])

    st.caption(result["priority"]["reason"])


    # ACTIONS
    st.subheader("Recommended Actions")

    for action in result["recommended_actions"]:

        st.success(action)


    # DISPATCH
    st.subheader("Dispatch Strategy")

    st.info(result["dispatch"]["strategy"])

    col1, col2 = st.columns(2)

    col1.metric(
        "Capacity Status",
        result["dispatch"]["capacity_status"]
    )

    col2.metric(
        "Next Step",
        result["dispatch"]["next_step"]
    )


    # IMPACT
    st.subheader("Impact")

    a, b, c = st.columns(3)

    a.metric(
        "Affected Employees",
        result["impact"]["affected_employees"]
    )

    b.metric(
        "Estimated Delay",
        result["impact"]["estimated_delay"]
    )

    c.metric(
        "Client Risk",
        result["impact"]["client_risk"]
    )


    # MESSAGES
    st.subheader("Ready Messages")

    hr, emp, drv = st.tabs(
        [
            "HR",
            "Employees",
            "Backup Driver"
        ]
    )

    with hr:
        st.text_area(
            "",
            result["messages"]["hr"],
            height=180
        )

    with emp:
        st.text_area(
            "",
            result["messages"]["employees"],
            height=180
        )

    with drv:
        st.text_area(
            "",
            result["messages"]["backup_driver"],
            height=180
        )


    # ESCALATION
    st.subheader("⚠ Human Decisions")

    if len(result["manual_decisions"]) == 0:

        st.success("No manual intervention required.")

    else:

        for decision in result["manual_decisions"]:

            st.warning(decision)
