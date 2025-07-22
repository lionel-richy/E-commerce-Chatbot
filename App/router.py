#from semantic_router import Route, RouteLayer
from semantic_router import Route
from semantic_router.encoders import HuggingFaceEncoder
from semantic_router.index import QdrantIndex
from semantic_router.index import LocalIndex
from semantic_router import SemanticRouter
from semantic_router.routers import SemanticRouter



#qdrant_index = QdrantIndex()


encoder = HuggingFaceEncoder(
    name="sentence-transformers/all-MiniLM-L6-v2"
)

# we could use this as a guide for our chatbot to avoid political conversations
faq = Route(
    name="faq",
    utterances=[
        "what is the return policy of the products?",
        "Do I get discount with the HDFC credit card?",
        "How can I track my order?",
        "What payement methods do you accept?",
        "How long does it take to process a refund ?",
        "Can I change my shipping address after placing an order?",
        "What is your cancellation policy?",
        "Do you deliver internationally?",
        "Where can I find my invoice or receipt?",
        "How do I apply a promo code?",
        "What should I do if I receive a defective product?",
        "What is your policy on defective products?",   
        "What is your policy on defective products?"
    ],
)


sql = Route(
    name='sql',
    utterances=[
        "I want to buy nike shoes that have 50% discount.",
        "Are there any shoes under Rs. 3000?",
        "Do you have formal shoes in size 9?",
        "Are there any Puma shoes on sale?",
        "What is the price of puma running shoes?",
        "What is the price of puma running shoes?",
        "Show me Adidas sneakers below $100",
        "I'm looking for red running shoes in size 8.",
        "Do you offer free shipping for orders above €50?",
        "Any discounted jackets for men?",
        "What is the stock status of Samsung Galaxy S21?",
        "Can you show me the latest iPhone models?",
        "What is the average rating of Nike shoes?",
        "What is the average rating of Nike shoes?"
    ]
)


index = LocalIndex()
#qdrant_index = QdrantIndex()
router = SemanticRouter(routes=[faq, sql], encoder= encoder, index=index,
    auto_sync="local")
#router.prepare_index()

if __name__ == "__main__":
    print(router("What is your policy on defective product?").name)
    print(router("Pink Puma shoes in price range 5000 to 1000").name)
    # Output: faq
    # Output: sql