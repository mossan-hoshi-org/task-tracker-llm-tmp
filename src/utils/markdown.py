from typing import List

from src.models.session import Session


def format_sessions_to_markdown(sessions: List[Session]) -> str:
    if not sessions:
        return "# Task Summary\n\nNo tasks recorded."

    markdown_lines = ["# Task Summary", ""]

    # Task list with durations
    markdown_lines.append("## Tasks")
    markdown_lines.append("")

    total_seconds: float = 0

    for session in sessions:
        duration = session.get_duration()
        total_seconds += duration

        hours = int(duration // 3600)
        minutes = int((duration % 3600) // 60)
        seconds = int(duration % 60)
        time_str = f"{hours:02d}:{minutes:02d}:{seconds:02d}"

        start_time = session.start_time.strftime("%Y-%m-%d %H:%M:%S") if session.start_time else "N/A"
        end_time = session.end_time.strftime("%Y-%m-%d %H:%M:%S") if session.end_time else "進行中"

        markdown_lines.append(f"- **{session.task_name}**: {time_str}")
        markdown_lines.append(f"  - Start: {start_time}")
        markdown_lines.append(f"  - End: {end_time}")
        markdown_lines.append("")

    # Total time
    total_hours = int(total_seconds // 3600)
    total_minutes = int((total_seconds % 3600) // 60)
    total_secs = int(total_seconds % 60)
    total_time_str = f"{total_hours:02d}:{total_minutes:02d}:{total_secs:02d}"

    markdown_lines.append(f"## Total Time: {total_time_str}")

    return "\n".join(markdown_lines)
