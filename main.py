"""Main simulator orchestration"""
import os
from datetime import datetime
from typing import Dict, List
from agents import CEO, ProjectManager, Developer
from evaluation import PerformanceEvaluator
from memory import MemoryManager
from utils.logger import setup_logger

logger = setup_logger(__name__)

class AIWorkforceSimulator:
    """Main simulator orchestrating multi-agent workflow"""
    
    def __init__(self):
        logger.info("Initializing AIWorkforceSimulator")
        self.ceo = CEO()
        self.pm = ProjectManager()
        self.developer = Developer()
        self.evaluator = PerformanceEvaluator()
        self.memory = MemoryManager()
        self.cycle_count = self.memory.memory_index.get("total_cycles", 0)
        logger.info(f"Simulator initialized. Previous cycles: {self.cycle_count}")
    
    def run_cycle(self, user_goal: str) -> Dict:
        """Execute one complete cycle of the organization"""
        
        self.cycle_count += 1
        logger.info(f"\n{'='*80}")
        logger.info(f"STARTING CYCLE {self.cycle_count}")
        logger.info(f"Goal: {user_goal}")
        logger.info(f"{'='*80}\n")
        
        cycle_data = {
            "cycle": self.cycle_count,
            "timestamp": datetime.now().isoformat(),
            "user_goal": user_goal,
            "stages": {}
        }
        
        try:
            # Stage 1: CEO Strategic Planning
            logger.info("Stage 1: CEO Strategic Planning")
            print("\n📊 CEO is developing strategy...")
            context = self.memory.get_context()
            strategy = self.ceo.generate_strategy(user_goal, context)
            cycle_data["stages"]["strategy"] = strategy
            logger.info("Strategy generated successfully")
            
            # Stage 2: PM Task Breakdown
            logger.info("Stage 2: PM Task Breakdown")
            print("📋 Project Manager is breaking down tasks...")
            context = self.memory.get_context()
            tasks = self.pm.break_down_tasks(strategy, context)
            cycle_data["stages"]["tasks"] = tasks
            logger.info("Tasks created successfully")
            
            # Stage 3: Developer Implementation Planning
            logger.info("Stage 3: Developer Implementation Planning")
            print("💻 Developer is planning implementation...")
            context = self.memory.get_context()
            implementation = self.developer.plan_implementation(tasks, context)
            cycle_data["stages"]["implementation"] = implementation
            logger.info("Implementation plan created successfully")
            
            # Stage 4: Evaluation
            logger.info("Stage 4: Evaluation")
            print("📊 Evaluating cycle performance...")
            evaluation = self.evaluator.evaluate_cycle(cycle_data)
            cycle_data["stages"]["evaluation"] = evaluation
            logger.info(f"Evaluation score: {evaluation.get('score', 'N/A')}")
            
            # Stage 5: Memory Update
            logger.info("Stage 5: Memory Update")
            reflection = {
                "strengths": evaluation.get("strengths", []),
                "areas_for_improvement": evaluation.get("areas_for_improvement", []),
                "lessons_learned": evaluation.get("lessons_learned", []),
                "recommendations": evaluation.get("recommendations", [])
            }
            self.memory.update(cycle_data, reflection)
            
            logger.info(f"✅ CYCLE {self.cycle_count} COMPLETE")
            logger.info(f"{'='*80}\n")
            
            return cycle_data
        
        except Exception as e:
            logger.error(f"Error during cycle execution: {e}", exc_info=True)
            raise
    
    def get_performance_metrics(self) -> Dict:
        """Get current performance metrics"""
        return self.memory.get_statistics()
    
    def get_cycle_history(self) -> List[Dict]:
        """Get all completed cycles"""
        return self.memory.memory_index.get("cycles", [])


if __name__ == "__main__":
    simulator = AIWorkforceSimulator()