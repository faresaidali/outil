from document_processor import DocumentProcessor
from solution_proposer import SolutionProposer
from result_presenter import ResultPresenter

def main():
    # Create instances of the core classes
    document_processor = DocumentProcessor()
    solution_proposer = SolutionProposer()
    result_presenter = ResultPresenter()

    # Process the input document or text
    document_processor.process_input()

    # Propose solutions based on the summarized content
    solution_proposer.propose_solutions(document_processor.summarized_content)

    # Present the generated result to the user
    result_presenter.present_result(solution_proposer.generated_result)

if __name__ == "__main__":
    main()
