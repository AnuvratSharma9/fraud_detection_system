from app.config import RISK_LEVELS

def get_risk_level(prob:float)->str:
    """
    COVERT FRAUD PROBABITLTY INTO A RISK LEVEL
    """
    if prob<RISK_LEVELS["LOW"]:
        return"LOW"
    elif prob< RISK_LEVELS["MEDIUM"]:
        return "MEDIUM"
    else:
        return "HIGH"
    
def get_action(risk_level:str)->str:
    """
    Convert risk level into a buisness action
    
    """
    if risk_level=="LOW":
        return "APPROVE"
    elif risk_level=="MEDIUM":
        return "MONITOR"
    else:
        return "MANUAL_REVIEW"