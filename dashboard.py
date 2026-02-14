"""Streamlit Dashboard for Simulator"""
import streamlit as st
import json
from datetime import datetime
from main import AIWorkforceSimulator

# Page configuration
st.set_page_config(
    page_title="AI Workforce Digital Twin Simulator",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom styling
st.markdown("""
    <style>
    .metric-card {
        background-color: #f0f2f6;
        padding: 20px;
        border-radius: 10px;
        margin: 10px 0;
    }
    .stage-header {
        background-color: #1f77e5;
        color: white;
        padding: 10px;
        border-radius: 5px;
        margin: 10px 0;
    }
    </style>
    """, unsafe_allow_html=True)

# Initialize session state
if "simulator" not in st.session_state:
    st.session_state.simulator = AIWorkforceSimulator()

if "cycles" not in st.session_state:
    st.session_state.cycles = []

# Header
st.title("🤖 AI Workforce Digital Twin Simulator")
st.markdown("---")

# Sidebar - Configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    user_goal = st.text_area(
        "Enter Your Goal:",
        height=150,
        placeholder="Example: Build a customer support chatbot using AI that reduces response time by 50% and improves satisfaction scores",
        key="goal_input"
    )
    
    col1, col2 = st.columns(2)
    with col1:
        run_button = st.button("🚀 Run Simulation", use_container_width=True, key="run_btn")
    with col2:
        clear_button = st.button("🗑️ Clear History", use_container_width=True, key="clear_btn")
    
    st.markdown("---")
    st.subheader("📈 Metrics Summary")
    
    metrics = st.session_state.simulator.get_performance_metrics()
    col1, col2 = st.columns(2)
    with col1:
        st.metric("Total Cycles", metrics.get("total_cycles", 0))
        st.metric("Improvement", f"{metrics.get('improvement', 0.0):.2f} points")
    with col2:
        st.metric("Avg Score", f"{metrics.get('average_score', 0.0):.2f}")
        st.metric("Best Score", f"{metrics.get('best_score', 0.0):.2f}")

# Main content area
if run_button:
    if not user_goal.strip():
        st.error("❌ Please enter a goal before running the simulation!")
    else:
        with st.spinner("🔄 Running simulation cycle..."):
            try:
                cycle_result = st.session_state.simulator.run_cycle(user_goal)
                st.session_state.cycles.append(cycle_result)
                st.success("✅ Cycle completed successfully!")
                
                # Display cycle results
                st.markdown(f"### Cycle {cycle_result['cycle']} - Results")
                
                # Tabs for different views
                tab1, tab2, tab3, tab4, tab5 = st.tabs(
                    ["📊 Strategy", "📋 Tasks", "💻 Implementation", "📈 Evaluation", "🔄 Reflection"]
                )
                
                with tab1:
                    st.subheader("CEO Strategic Plan")
                    strategy = cycle_result["stages"]["strategy"]
                    if "raw_response" in strategy:
                        st.info(strategy["raw_response"])
                    else:
                        col1, col2 = st.columns(2)
                        with col1:
                            st.write("**Vision:**", strategy.get("vision", "N/A"))
                            st.write("**Mission:**", strategy.get("mission", "N/A"))
                        with col2:
                            st.write("**Timeline:**", strategy.get("timeline", "N/A"))
                            st.write("**Confidence:**", strategy.get("confidence_level", "N/A"))
                        
                        st.write("**Key Objectives:**")
                        for obj in strategy.get("key_objectives", []):
                            st.write(f"- {obj}")
                        
                        st.write("**Success Metrics:**")
                        for metric in strategy.get("success_metrics", []):
                            st.write(f"- {metric}")
                
                with tab2:
                    st.subheader("PM Task Breakdown")
                    tasks = cycle_result["stages"]["tasks"]
                    if "raw_response" in tasks:
                        st.info(tasks["raw_response"])
                    else:
                        st.write(f"**Project:** {tasks.get('project_name', 'N/A')}")
                        st.write(f"**Total Tasks:** {tasks.get('total_tasks', 'N/A')}")
                        st.write(f"**Estimated Duration:** {tasks.get('estimated_duration', 'N/A')}")
                        
                        st.write("**Tasks:**")
                        for task in tasks.get("tasks", []):
                            with st.expander(f"{task.get('task_id', 'N/A')} - {task.get('title', 'N/A')}"):
                                st.write(f"**Description:** {task.get('description', 'N/A')}")
                                st.write(f"**Effort:** {task.get('effort_estimate', 'N/A')}")
                                st.write(f"**Priority:** {task.get('priority', 'N/A')}")
                                st.write("**Success Criteria:**")
                                for criteria in task.get("success_criteria", []):
                                    st.write(f"- {criteria}")
                
                with tab3:
                    st.subheader("Developer Implementation Plan")
                    impl = cycle_result["stages"]["implementation"]
                    if "raw_response" in impl:
                        st.info(impl["raw_response"])
                    else:
                        st.write("**Technical Approach:**", impl.get("technical_approach", "N/A"))
                        st.write("**Technology Stack:**", ", ".join(impl.get("technology_stack", [])))
                        
                        st.write("**Testing Strategy:**")
                        test_strat = impl.get("testing_strategy", {})
                        st.write(f"- Unit Tests: {test_strat.get('unit_tests', 'N/A')}")
                        st.write(f"- Integration Tests: {test_strat.get('integration_tests', 'N/A')}")
                        st.write(f"- Coverage Target: {test_strat.get('coverage_target', 'N/A')}")
                        
                        st.write("**Technical Debt:**")
                        tech_debt = impl.get("technical_debt", {})
                        st.write(f"- Priority: {tech_debt.get('priority', 'N/A')}")
                        st.write(f"- Mitigation: {tech_debt.get('mitigation_plan', 'N/A')}")
                
                with tab4:
                    st.subheader("Performance Evaluation")
                    eval_data = cycle_result["stages"]["evaluation"]
                    
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Overall Score", f"{eval_data.get('score', 0):.2f}/10")
                    with col2:
                        st.metric("Strategy Quality", eval_data.get("scores", {}).get("strategy_quality", "N/A"))
                    with col3:
                        st.metric("Task Clarity", eval_data.get("scores", {}).get("task_clarity", "N/A"))
                    
                    st.write("**Strengths:**")
                    for strength in eval_data.get("strengths", []):
                        st.write(f"✅ {strength}")
                    
                    st.write("**Areas for Improvement:**")
                    for area in eval_data.get("areas_for_improvement", []):
                        st.write(f"⚠️ {area}")
                    
                    if eval_data.get("critical_feedback"):
                        st.warning(f"🔴 Critical Feedback: {eval_data.get('critical_feedback')}")
                
                with tab5:
                    st.subheader("Reflection & Learning")
                    eval_data = cycle_result["stages"]["evaluation"]
                    
                    st.write("**Lessons Learned:**")
                    for lesson in eval_data.get("lessons_learned", []):
                        st.write(f"📚 {lesson}")
                    
                    st.write("**Recommendations for Next Cycle:**")
                    for rec in eval_data.get("recommendations", []):
                        st.write(f"💡 {rec}")
            
            except Exception as e:
                st.error(f"❌ Error during simulation: {str(e)}")
                st.error("Please check your OpenAI API key and try again.")

# History section
if st.session_state.cycles:
    st.markdown("---")
    st.subheader("📜 Cycle History")
    
    history_data = []
    for cycle in st.session_state.cycles:
        history_data.append({
            "Cycle": cycle["cycle"],
            "Goal": cycle["user_goal"][:50] + "..." if len(cycle["user_goal"]) > 50 else cycle["user_goal"],
            "Score": f"{cycle['stages']['evaluation'].get('score', 0):.2f}",
            "Time": datetime.fromisoformat(cycle["timestamp"]).strftime("%Y-%m-%d %H:%M:%S")
        })
    
    st.dataframe(history_data, use_container_width=True)

if clear_button:
    st.session_state.cycles = []
    st.success("✅ History cleared!")
    st.rerun()

# Footer
st.markdown("---")
st.markdown("""
### About This Simulator
This AI Workforce Digital Twin Simulator demonstrates a multi-agent AI organization with:
- **CEO Agent**: Strategic planning and direction setting
- **Project Manager Agent**: Task breakdown and project planning
- **Developer Agent**: Implementation planning and technical design
- **Evaluator**: Performance assessment and feedback
- **Memory System**: Persistent learning across cycles

Each cycle represents one complete organizational workflow from goal to evaluation.
""")