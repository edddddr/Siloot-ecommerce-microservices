import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
from catalog.models import Product


def build_product_matrix():
    products = Product.objects.filter(is_active=True)

    product_ids = []
    feature_matrix = []

    for product in products:
        # Simple feature vector:
        # [price, stock, category_id]
        vector = [
            float(product.price),
            float(product.stock),
            float(product.category_id),
        ]
        product_ids.append(product.id)
        feature_matrix.append(vector)

    return product_ids, np.array(feature_matrix)


def recommend_for_user(purchased_ids, top_k=5):
    product_ids, matrix = build_product_matrix()

    if not purchased_ids:
        return product_ids[:top_k]

    # Find vectors of purchased products
    purchased_indices = [
        product_ids.index(pid)
        for pid in purchased_ids
        if pid in product_ids
    ]

    if not purchased_indices:
        return product_ids[:top_k]

    purchased_vectors = matrix[purchased_indices]

    # Average user profile vector
    user_vector = np.mean(purchased_vectors, axis=0).reshape(1, -1)

    similarities = cosine_similarity(user_vector, matrix)[0]

    # Rank products by similarity
    ranked_indices = similarities.argsort()[::-1]

    recommended_ids = []
    for idx in ranked_indices:
        pid = product_ids[idx]
        if pid not in purchased_ids:
            recommended_ids.append(pid)
        if len(recommended_ids) == top_k:
            break

    return recommended_ids
