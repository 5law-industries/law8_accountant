"""hCaptcha Streamlit component."""

from typing import Optional


def hcaptcha(
    site_key: str,
    key: Optional[str] = None,
    theme: str = "light",
    size: str = "normal",
) -> Optional[str]:
    """
    Render hCaptcha widget (stub implementation).
    
    Args:
        site_key: hCaptcha site key.
        key: Widget key for Streamlit.
        theme: Widget theme (light/dark).
        size: Widget size (normal/compact).
    
    Returns:
        Optional captcha token.
    
    Note:
        This is a stub implementation. For production use, implement
        the actual Streamlit component with React/Vite frontend.
    """
    # Stub implementation - returns None to indicate no captcha verification
    # In production, this would render the actual hCaptcha widget
    return None


__all__ = ["hcaptcha"]
