from app.rag.retrieval import search_documents


TEST_CASES = [
    # 1. Direct fact lookup
    {
        "category": "Direct fact lookup",
        "query": "When was W3 Engineers founded?",
        "expected": "2009",
        "sections": ["1"],
    },
    {
        "category": "Direct fact lookup",
        "query": "Where is the headquarters?",
        "expected": "Dhaka, Bangladesh",
        "sections": ["1"],
    },
    {
        "category": "Direct fact lookup",
        "query": "What is the full office address?",
        "expected": "World Business Centrum, 4th Floor, 76/A, Banani-11, Dhaka-1213",
        "sections": ["4"],
    },
    {
        "category": "Direct fact lookup",
        "query": "What are the office hours?",
        "expected": "Mon–Fri, 10:00 AM–7:00 PM (GMT+6)",
        "sections": ["4"],
    },
    {
        "category": "Direct fact lookup",
        "query": "What type of organization is W3 Engineers?",
        "expected": "Privately held",
        "sections": ["1"],
    },
    {
        "category": "Direct fact lookup",
        "query": "What is the company's LinkedIn page?",
        "expected": "linkedin.com/company/w3engineers/",
        "sections": ["1", "9"],
    },

    # 2. List retrieval
    {
        "category": "List retrieval",
        "query": "What products does W3 Engineers offer?",
        "expected": (
            "rentbyowner.com, Telemesh, WorkAny, qEASY, MyProperty, "
            "Whipy, Lend It Right, Bike Insurance, Ask It"
        ),
        "sections": ["3"],
    },
    {
        "category": "List retrieval",
        "query": "What AI services does the company provide?",
        "expected": (
            "AI, ML, Predictive Recommendations, Image Labeling and "
            "Captioning, Data Engineering, Travel Data Integration"
        ),
        "sections": ["2"],
    },
    {
        "category": "List retrieval",
        "query": "What celebrations and activities does the company have?",
        "expected": (
            "Birthdays, festivals, annual get-togethers, team building, "
            "team parties"
        ),
        "sections": ["8"],
    },

    # 3. Numeric and detail questions
    {
        "category": "Numeric and detail questions",
        "query": "How much of the lunch cost do employees pay?",
        "expected": "20% (the company covers 80%)",
        "sections": ["7"],
    },
    {
        "category": "Numeric and detail questions",
        "query": "How long is the internship training phase?",
        "expected": "2 months, followed by 2 months of team assignment",
        "sections": ["5"],
    },
    {
        "category": "Numeric and detail questions",
        "query": "What recreation facilities are available?",
        "expected": "Table tennis and foosball",
        "sections": ["7"],
    },

    # 4. Paraphrased or semantic queries
    {
        "category": "Paraphrased / semantic queries",
        "query": "Do employees get meals at the office?",
        "expected": "Free breakfast and evening snacks; 80% of lunch covered",
        "sections": ["7"],
    },
    {
        "category": "Paraphrased / semantic queries",
        "query": "What happens after the intern's first few months?",
        "expected": "Evaluation, then assignment to a team for 2 more months",
        "sections": ["5"],
    },
    {
        "category": "Paraphrased / semantic queries",
        "query": "Can I learn how to build chatbots or agents there?",
        "expected": "LangChain, LangGraph, agent workflows, tool calling",
        "sections": ["6.5"],
    },
    {
        "category": "Paraphrased / semantic queries",
        "query": "Does the company work on blockchain or VR?",
        "expected": "Yes, both are listed",
        "sections": ["2"],
    },
    {
        "category": "Paraphrased / semantic queries",
        "query": "Is there somewhere to rent a property on your platform?",
        "expected": "rentbyowner.com, possibly MyProperty",
        "sections": ["3"],
    },

    # 5. Topic-specific training queries
    {
        "category": "Topic-specific training",
        "query": "Which web scraping tools are taught?",
        "expected": "Scrapy, Scrapyd, Docker, plus export formats",
        "sections": ["6.3"],
    },
    {
        "category": "Topic-specific training",
        "query": "What testing tools are covered?",
        "expected": "Playwright, Pytest, Allure, GitHub Actions",
        "sections": ["6.4"],
    },
    {
        "category": "Topic-specific training",
        "query": "Which vector database is used?",
        "expected": "ChromaDB",
        "sections": ["6.5"],
    },
    {
        "category": "Topic-specific training",
        "query": "Which third-party APIs are covered?",
        "expected": "Ticketmaster API, Google Places API",
        "sections": ["6.2"],
    },
    {
        "category": "Topic-specific training",
        "query": "What backend frameworks are covered?",
        "expected": "Flask, FastAPI, Beego",
        "sections": ["6.1"],
    },

    # 6. Multi-chunk and ambiguous queries
    {
        "category": "Multi-chunk / ambiguous queries",
        "query": "Where is Docker used in the training?",
        "expected": "Docker is mentioned in sections 6.3 and 6.4",
        "sections": ["6.3", "6.4"],
        "k": 10,
    },
    {
        "category": "Multi-chunk / ambiguous queries",
        "query": "Which sections mention Python?",
        "expected": "Sections 6.1, 6.3, and 6.4",
        "sections": ["6.1", "6.3", "6.4"],
        "k": 10,
    },
    {
        "category": "Multi-chunk / ambiguous queries",
        "query": "Summarize the internship program end to end.",
        "expected": "Combine internship structure (5), training topics (6), and benefits (7)",
        "sections": ["5", "6", "7"],
        "k": 10,
    },

    # 7. Caveat and confidence queries
    {
        "category": "Caveat / confidence queries",
        "query": "Is the 2+2 month internship structure official policy?",
        "expected": (
            "No. It is based on firsthand experience, "
            "not a confirmed universal policy."
        ),
        "sections": ["5"],
    },
    {
        "category": "Caveat / confidence queries",
        "query": "Is there an official internship syllabus?",
        "expected": "No. The topics are inferred, not an official syllabus.",
        "sections": ["6"],
        "k": 10,
    },
    {
        "category": "Caveat / confidence queries",
        "query": "Are the lunch and snack benefits company policy?",
        "expected": (
            "Unverified. They come from an intern's firsthand experience."
        ),
        "sections": ["7"],
    },

    # 8. Negative tests
    {
        "category": "Negative tests",
        "query": "What is the internship stipend or salary?",
        "expected": "Not in the document",
        "sections": [],
    },
    {
        "category": "Negative tests",
        "query": "How do I apply for the internship?",
        "expected": "Application process is not in the document",
        "sections": [],
    },
    {
        "category": "Negative tests",
        "query": "What GitHub projects did interns build?",
        "expected": "Not in the document",
        "sections": [],
    },
    {
        "category": "Negative tests",
        "query": "How many employees work at W3 Engineers?",
        "expected": "Not in the document",
        "sections": [],
    },
    {
        "category": "Negative tests",
        "query": "Who is the CEO?",
        "expected": "Not in the document",
        "sections": [],
    },
    {
        "category": "Negative tests",
        "query": "What is the Wi-Fi password, dress code, or leave policy?",
        "expected": "Not in the document",
        "sections": [],
    },
]


def run_retrieval_tests() -> None:
    """Run all retrieval test cases and display ranked results.

    Function: run_retrieval_tests
    Args:
        None.
    Returns:
        None: Prints expected information and retrieved document chunks.
    """
    for index, test_case in enumerate(TEST_CASES, start=1):
        query = test_case["query"]
        k = test_case.get("k", 3)

        print("\n" + "=" * 90)
        print(f"TEST {index}/{len(TEST_CASES)}")
        print(f"Category: {test_case['category']}")
        print(f"Query: {query}")
        print(f"Expected answer: {test_case['expected']}")
        print(f"Expected sections: {test_case['sections']}")
        print(f"Retrieval top-k: {k}")
        print("-" * 90)

        results = search_documents(query, k=k)

        if not results:
            print("No documents retrieved.")
            continue

        for rank, document in enumerate(results, start=1):
            metadata = document.metadata

            print(f"\n--- Rank {rank} ---")
            print(f"Source: {metadata.get('source', 'Unknown')}")
            print(f"Pages: {metadata.get('pages', [])}")
            print(f"Section ID: {metadata.get('section_id', 'Unknown')}")
            print(f"Section Title: {metadata.get('section_title', 'Unknown')}")
            print(f"Parent Section ID: {metadata.get('parent_section_id', 'None')}")
            print(f"Parent Section Title: {metadata.get('parent_section_title', 'None')}")
            print(f"Content:\n{document.page_content}")

    print("\n" + "=" * 90)
    print(f"Completed {len(TEST_CASES)} retrieval test cases.")


if __name__ == "__main__":
    run_retrieval_tests()