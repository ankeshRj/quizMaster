import random
from typing import List, Dict, Tuple
from dataclasses import dataclass
from enum import Enum


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


@dataclass
class Question:
    text: str
    options: List[str]
    answer: int
    difficulty: Difficulty = Difficulty.MEDIUM
    
    def is_correct(self, user_answer: int) -> bool:
        return user_answer == self.answer


@dataclass
class Player:
    name: str
    score: int = 0
    
    def add_point(self):
        self.score += 1
    
    def get_percentage(self, total_questions: int) -> float:
        return (self.score / total_questions * 100) if total_questions > 0 else 0


class QuizGame:
    def __init__(self):
        self.questions = self._load_questions()
        self.players: List[Player] = []
    
    def _load_questions(self) -> List[Question]:
        """Load and return all quiz questions."""
        return [
            Question("What is the capital of France?", 
                    ["London", "Berlin", "Paris", "Madrid"], 3, Difficulty.EASY),
            Question("Which planet is known as the Red Planet?", 
                    ["Earth", "Mars", "Jupiter", "Venus"], 2, Difficulty.EASY),
            Question("What is the largest ocean on Earth?", 
                    ["Atlantic", "Indian", "Arctic", "Pacific"], 4, Difficulty.EASY),
            Question("Who wrote 'Hamlet'?", 
                    ["Charles Dickens", "William Shakespeare", "Leo Tolstoy", "Mark Twain"], 2, Difficulty.MEDIUM),
            Question("Which element has the chemical symbol 'O'?", 
                    ["Gold", "Oxygen", "Silver", "Zinc"], 2, Difficulty.EASY),
            Question("In which year did the Titanic sink?", 
                    ["1905", "1912", "1920", "1898"], 2, Difficulty.MEDIUM),
            Question("What is the tallest mountain in the world?", 
                    ["K2", "Kanchenjunga", "Everest", "Lhotse"], 3, Difficulty.EASY),
            Question("Who painted the Mona Lisa?", 
                    ["Vincent van Gogh", "Leonardo da Vinci", "Pablo Picasso", "Michelangelo"], 2, Difficulty.MEDIUM),
            Question("Which country is the origin of the car brand 'Toyota'?", 
                    ["South Korea", "China", "Germany", "Japan"], 4, Difficulty.MEDIUM),
            Question("Which gas do plants absorb from the atmosphere?", 
                    ["Oxygen", "Nitrogen", "Carbon Dioxide", "Helium"], 3, Difficulty.EASY)
        ]
    
    def print_welcome(self):
        """Display welcome banner."""
        banner = """
╔═══════════════════════════════════════╗
║      Welcome to QuizMaster Pro!      ║
║   Put your knowledge to the test!    ║
╚═══════════════════════════════════════╝
        """
        print(banner)
    
    def get_player_name(self, player_num: int) -> str:
        """Get and validate a single player name."""
        while True:
            name = input(f"Enter name for Player {player_num}: ").strip()
            if name:
                return name
            print("Name cannot be empty. Please try again.")
    
    def setup_players(self, num_players: int):
        """Initialize players for the game."""
        self.players = [Player(self.get_player_name(i + 1)) for i in range(num_players)]
    
    def display_question(self, question: Question, q_number: int, player_name: str = None):
        """Display a question with its options."""
        print("\n" + "=" * 50)
        player_text = f"[{player_name}'s turn] " if player_name else ""
        print(f"Question {q_number}: {player_text}{question.text}")
        print("-" * 50)
        for i, option in enumerate(question.options, 1):
            print(f"  {i}. {option}")
        print("=" * 50)
    
    def get_answer(self, num_options: int) -> int:
        """Get and validate user's answer."""
        while True:
            try:
                answer = input(f"Your answer (1-{num_options}): ").strip()
                answer_num = int(answer)
                if 1 <= answer_num <= num_options:
                    return answer_num
                print(f"Please enter a number between 1 and {num_options}.")
            except ValueError:
                print("Invalid input! Please enter a number.")
    
    def provide_feedback(self, question: Question, user_answer: int, is_correct: bool):
        """Provide feedback on the answer."""
        if is_correct:
            print("✓ Correct! 🎉")
        else:
            correct_answer = question.options[question.answer - 1]
            print(f"✗ Incorrect. The correct answer was: {question.answer}. {correct_answer}")
    
    def display_scores(self):
        """Display current scores for all players."""
        print("\n📊 Current Scores:")
        for player in self.players:
            print(f"  • {player.name}: {player.score}")
        print()
    
    def display_final_results(self, total_questions: int):
        """Display final game results."""
        print("\n" + "=" * 50)
        print("🏁 GAME OVER - Final Results")
        print("=" * 50)
        
        for player in self.players:
            percentage = player.get_percentage(total_questions)
            print(f"{player.name}: {player.score}/{total_questions} ({percentage:.1f}%)")
        
        if len(self.players) > 1:
            winner = max(self.players, key=lambda p: p.score)
            if all(p.score == winner.score for p in self.players):
                print("\n🤝 It's a tie! Well played everyone!")
            else:
                print(f"\n🏆 Congratulations {winner.name}, you win!")
        
        print("=" * 50)
    
    def play_round(self, questions: List[Question]):
        """Play a complete round of questions."""
        player_idx = 0
        
        for i, question in enumerate(questions, 1):
            current_player = self.players[player_idx] if len(self.players) > 1 else self.players[0]
            
            self.display_question(question, i, current_player.name if len(self.players) > 1 else None)
            user_answer = self.get_answer(len(question.options))
            is_correct = question.is_correct(user_answer)
            
            if is_correct:
                current_player.add_point()
            
            self.provide_feedback(question, user_answer, is_correct)
            
            if len(self.players) == 1:
                print(f"Score: {current_player.score}/{i}")
            else:
                self.display_scores()
                player_idx = (player_idx + 1) % len(self.players)
    
    def get_game_mode(self) -> str:
        """Get the game mode from user."""
        while True:
            print("\n🎮 Game Modes:")
            print("  1 - Single Player")
            print("  2 - Two Players")
            print("  Q - Quit")
            
            choice = input("\nSelect mode: ").strip().lower()
            if choice in ['1', '2', 'q']:
                return choice
            print("Invalid choice! Please enter 1, 2, or Q.")
    
    def ask_replay(self) -> bool:
        """Ask if user wants to play again."""
        while True:
            choice = input("\n🔄 Play again? (y/n): ").strip().lower()
            if choice in ['y', 'n']:
                return choice == 'y'
            print("Please enter 'y' or 'n'.")
    
    def run(self):
        """Main game loop."""
        self.print_welcome()
        
        while True:
            mode = self.get_game_mode()
            
            if mode == 'q':
                print("\n👋 Thanks for playing QuizMaster! Goodbye!")
                break
            
            # Setup game
            num_players = int(mode)
            self.setup_players(num_players)
            
            # Optionally shuffle questions for variety
            game_questions = self.questions.copy()
            random.shuffle(game_questions)
            
            # Play the round
            print(f"\n🎯 Starting game with {num_players} player{'s' if num_players > 1 else ''}!")
            self.play_round(game_questions)
            
            # Show final results
            self.display_final_results(len(game_questions))
            
            # Ask to replay
            if not self.ask_replay():
                print("\n👋 Thanks for playing QuizMaster! Goodbye!")
                break


def main():
    game = QuizGame()
    game.run()


if __name__ == "__main__":
    main()
