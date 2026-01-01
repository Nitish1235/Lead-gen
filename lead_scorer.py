"""
Lead scoring and value justification generator
"""
from typing import Dict, Optional
import config


class LeadScorer:
    """Calculates lead scores and generates value justifications"""
    
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
    
    def generate_justification(
        self,
        business_name: str,
        has_phone: bool,
        has_email: bool,
        rating: Optional[float],
        review_count: Optional[int],
        website_analysis: Dict,
        category: str,
    ) -> str:
        """
        Generate human-readable value justification
        
        Args:
            business_name: Name of the business
            has_phone: Whether business has phone
            has_email: Whether business has email
            rating: Google rating
            review_count: Number of reviews
            website_analysis: Website analysis results
            category: Business category
            
        Returns:
            Short justification text
        """
        reasons = []
        
        # Contact accessibility
        if has_phone:
            reasons.append("direct phone contact available")
        if has_email:
            reasons.append("email accessible")
        
        # Rating insights
        if rating is not None:
            if rating < 3.5:
                reasons.append(f"low rating ({rating:.1f}) suggests improvement needed")
            elif rating < 4.0:
                reasons.append(f"moderate rating ({rating:.1f}) indicates potential for enhancement")
        
        if review_count is not None and review_count < 50:
            reasons.append("growing business with room for digital expansion")
        
        # Website issues (opportunities)
        platform = website_analysis.get("platform", "unknown")
        if platform in ["Wix", "WordPress", "GoDaddy Website Builder"]:
            reasons.append(f"uses basic platform ({platform}) - modernization opportunity")
        
        if not website_analysis.get("has_online_booking", False):
            reasons.append("no online booking system - automation opportunity")
        
        if not website_analysis.get("has_https", False):
            reasons.append("lacks HTTPS - security/trust improvement needed")
        
        if website_analysis.get("is_weak_website", False):
            reasons.append("website needs modernization")
        
        if website_analysis.get("has_whatsapp", False):
            reasons.append("uses WhatsApp - ready for digital tools")
        
        # Category-specific insights
        category_lower = category.lower()
        
        # Hospitality & Food
        if category_lower in ["restaurant", "cafe", "catering service", "food truck"]:
            reasons.append("hospitality sector benefits from booking/reservation systems")
        
        # Healthcare & Wellness
        elif category_lower in ["dental clinic", "medical clinic", "doctor office", "veterinary clinic", 
                                "physiotherapy clinic", "chiropractic clinic", "massage therapy", 
                                "acupuncture clinic", "psychology clinic", "counseling center"]:
            reasons.append("healthcare sector needs secure, compliant digital solutions and appointment systems")
        
        # Beauty & Personal Care (high appointment value)
        elif category_lower in ["beauty salon", "hair salon", "barber shop", "nail salon", "spa", 
                                "esthetician", "tattoo parlor", "piercing studio", "laser hair removal", 
                                "cosmetic clinic", "pet grooming"]:
            reasons.append("appointment-based business that benefits from online booking and CRM")
        
        # Fitness & Sports
        elif category_lower in ["fitness center", "gym", "yoga studio", "pilates studio", 
                               "martial arts school", "dance studio", "personal trainer"]:
            reasons.append("fitness business benefits from membership management and class scheduling")
        
        # Professional Services
        elif category_lower in ["law firm", "accounting firm", "consulting firm", "financial advisor", 
                               "insurance agency", "real estate agency", "real estate agent", 
                               "mortgage broker", "tax preparer"]:
            reasons.append("professional service that benefits from CRM, scheduling, and client management")
        
        # Education & Training
        elif category_lower in ["coaching institute", "tutoring center", "driving school", 
                               "music school", "language school", "art school", "training center", "bootcamp"]:
            reasons.append("education business needs scheduling, student management, and payment systems")
        
        # Home Services
        elif category_lower in ["plumber", "electrician", "hvac contractor", "handyman", "carpenter", 
                               "roofer", "painter", "landscaping service", "lawn care service", 
                               "cleaning service", "moving company", "locksmith", "appliance repair"]:
            reasons.append("service business that benefits from scheduling, dispatch, and customer management")
        
        # Automotive Services
        elif category_lower in ["auto repair shop", "car mechanic", "auto body shop", "car wash", 
                               "tire shop", "auto detailing", "computer repair", "phone repair"]:
            reasons.append("service business benefits from appointment scheduling and customer tracking")
        
        # Photography & Events
        elif category_lower in ["photography studio", "wedding photographer", "event planner", 
                               "caterer", "florist", "dj service", "party rental"]:
            reasons.append("event-based business needs booking, calendar management, and client communication")
        
        # Retail & E-commerce
        elif category_lower in ["e-commerce store", "retail store", "boutique", "jewelry store", 
                               "furniture store", "pet store"]:
            reasons.append("retail business benefits from inventory management and online presence")
        
        # Creative & Media
        elif category_lower in ["digital marketing agency", "web design agency", "graphic design studio", 
                               "advertising agency", "video production", "printing service"]:
            reasons.append("creative agency benefits from project management and client portals")
        
        if not reasons:
            reasons.append("local business with digital growth potential")
        
        # Combine into readable text
        if len(reasons) == 1:
            return reasons[0].capitalize() + "."
        elif len(reasons) == 2:
            return f"{reasons[0].capitalize()} and {reasons[1]}."
        else:
            main_reasons = reasons[:3]  # Top 3 reasons
            return f"{main_reasons[0].capitalize()}, {main_reasons[1]}, and {main_reasons[2]}."

