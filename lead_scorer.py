"""
Lead scoring generator
"""
from typing import Dict, Optional
import config


class LeadScorer:
    """Calculates lead scores"""
    
    def __init__(self):
        self.weights = config.SCORE_WEIGHTS
    
    def calculate_score(
        self,
        has_phone: bool,
        has_email: bool,
        has_address: bool,
        rating: Optional[float],
        review_count: Optional[int],
        website_analysis: Dict,
    ) -> int:
        """
        Calculate lead score based on quality signals
        
        Args:
            has_phone: Whether business has phone number
            has_email: Whether business has email
            has_address: Whether business has address
            rating: Google rating (0-5)
            review_count: Number of reviews
            website_analysis: Results from website analyzer
            
        Returns:
            Lead score (0-100+)
        """
        score = 0
        
        # Contact information
        if has_phone:
            score += self.weights["has_phone"]
        if has_email:
            score += self.weights["has_email"]
        if has_address:
            score += self.weights["has_address"]
        
        # Rating signals (lower rating = more likely to need help)
        if rating is not None:
            if rating < 3.5:
                score += self.weights["low_rating"]
            elif rating < 4.0:
                score += self.weights["medium_rating"]
        
        # Review count (fewer reviews = newer/smaller business = potential client)
        if review_count is not None and review_count < 50:
            score += self.weights["few_reviews"]
        
        # Website quality signals
        platform = website_analysis.get("platform", "unknown")
        if platform in ["Wix", "WordPress", "GoDaddy Website Builder", "Weebly"]:
            score += self.weights["outdated_platform"]
        
        if not website_analysis.get("has_online_booking", False):
            score += self.weights["no_online_booking"]
        
        if not website_analysis.get("has_https", False):
            score += self.weights["no_https"]
        
        if website_analysis.get("is_weak_website", False):
            score += self.weights["weak_website"]
        
        return min(score, 150)  # Cap at 150 for readability

