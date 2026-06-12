# Re-exporta componentes UI reutilizables / Re-exports reusable UI components

from app.components.ui_blocks import QBlock, InsightBox, ScoreBadge, plotly_iframe
from app.components.kpi_cards import KPICard
from app.components.sidebar   import AppSidebar

__all__ = ["QBlock", "InsightBox", "ScoreBadge", "plotly_iframe", "KPICard", "AppSidebar"]
