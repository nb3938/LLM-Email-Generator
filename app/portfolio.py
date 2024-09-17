import pandas as pd  # Import pandas for data handling
import chromadb  # Import ChromaDB for vector store operations
import uuid  # Import uuid for generating unique identifiers


class Portfolio:
    # Constructor to initialize Portfolio object with default CSV file and ChromaDB settings
    def __init__(self, file_path="app/resource/my_portfolio.csv"):
        self.file_path = file_path  
        self.data = pd.read_csv(file_path)  
        # Initialize ChromaDB Persistent Client for storing and querying the portfolio data
        self.chroma_client = chromadb.PersistentClient('vectorstore')
        # Create or retrieve a collection named "portfolio" in the vector store
        self.collection = self.chroma_client.get_or_create_collection(name="portfolio")

    # Method to load the portfolio data into ChromaDB collection
    def load_portfolio(self):
        # If the collection is empty, add the portfolio data
        if not self.collection.count():
            # Iterate over each row in the portfolio DataFrame
            for _, row in self.data.iterrows():
                # Add the Techstack as the document, and Links as metadata into the collection
                self.collection.add(documents=row["Techstack"],
                                    metadatas={"links": row["Links"]},
                                    ids=[str(uuid.uuid4())])  # Assign a unique ID using uuid4

    # Method to query portfolio links based on provided skills
    def query_links(self, skills):
        # Perform a query on the ChromaDB collection using the skills, and return the metadata
        return self.collection.query(query_texts=skills, n_results=2).get('metadatas', [])

