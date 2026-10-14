"""Cosmo Engineering multi-agent pipeline (PM -> Design -> Cost -> QA)."""

from .pipeline import PipelineResult, run_pipeline

__all__ = ["run_pipeline", "PipelineResult"]
