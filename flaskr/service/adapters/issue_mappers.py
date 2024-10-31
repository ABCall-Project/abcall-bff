from typing import Any, Union, Dict

def issues_pagination_mapper(issue_response: Union[Dict[str, Any], None]):
    return {
        "page": issue_response.get("page"),
        "limit": issue_response.get("limit"),
        "totalPages": issue_response.get("total_pages"),
        "hasNext": issue_response.get("has_next"),
        "data": [{
            "id": item.get("id"),
            "authUserId": item.get("auth_user_id"),
            "status": item.get("status"),
            "subject": item.get("subject"),
            "description": item.get("description"),
            "createdAt": item.get("created_at"),
            "closedAt": item.get("closed_at"),
            "channelPlanId": item.get("channel_plan_id")
        } for item in issue_response.get("data", [])]
    }
