from typing import Optional, Dict, List
from config import get_supabase


class ReportDAO:

    def __init__(self):
        self.sb = get_supabase()
        self.table = "report0"

    def create_report(
        self,
        report_type: str,
        details: Dict
    ) -> Dict:

        payload = {
            "report_type": report_type,
            "details": details
        }

        resp = (
            self.sb.table(self.table)
            .insert(payload)
            .execute()
        )

        return resp.data[0] if resp.data else {}

    def get_report(
        self,
        report_id: int
    ) -> Optional[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .eq("report_id", report_id)
            .limit(1)
            .execute()
        )

        return resp.data[0] if resp.data else None

    def list_reports(
        self,
        limit: int = 100
    ) -> List[Dict]:

        resp = (
            self.sb.table(self.table)
            .select("*")
            .order("report_id")
            .limit(limit)
            .execute()
        )

        return resp.data or []

    def delete_report(
        self,
        report_id: int
    ) -> Optional[Dict]:

        report = self.get_report(
            report_id
        )

        if not report:
            return None

        self.sb.table(
            self.table
        ).delete().eq(
            "report_id",
            report_id
        ).execute()

        return report
