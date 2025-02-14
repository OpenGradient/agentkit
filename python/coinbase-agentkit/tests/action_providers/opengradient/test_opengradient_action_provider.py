"""Tests for OpenGradient action provider."""

from unittest.mock import MagicMock, patch

import pytest
from pydantic import ValidationError
from coinbase_agentkit.action_providers.opengradient.schemas import (
    OpenGradientReadWorkflow,
)
from coinbase_agentkit.action_providers.opengradient.opengradient_action_provider import opengradient_action_provider

from coinbase_agentkit.network import Network

import opengradient as og

TEST_OG_PRIVATE_KEY = ""
ETH_FORECASE_ADDRESS = ""
BTC_FORECAST_ADDRESS = "0x6e0641925b845A1ca8aA9a890C4DEF388E9197e0"


def test_error_provider_init():
    """Test that the opengradient action provider will not intialize if no private key is provided"""
    with pytest.raises(ValueError) as excinfo:
        provider = opengradient_action_provider()
    assert "OPENGRADIENT_PRIVATE_KEY" in str(excinfo.value)

@pytest.mark.usefixtures("mock_env")
def test_successful_provider_init():
    """Test that the opengradient action provider can be initialized correctly."""
    provider = opengradient_action_provider()

def test_bad_read_workflow_schema():
    """Test that the read workflow schema fails with invalid arguments."""
    with pytest.raises(ValidationError):
        OpenGradientReadWorkflow()

def test_successful_read_workflow_schema():
    """Test that the read workflow schema accepts valid arguments."""
    args = {
        "contract_address" : BTC_FORECAST_ADDRESS
    }
    inputs = OpenGradientReadWorkflow(**args)
    assert inputs.contract_address == args["contract_address"]

@pytest.mark.usefixtures("mock_env")
def test_bad_address_read_workflow_action():
    """Test that the read workflow tool fails when an invalid smart contract address is provided."""
    provider = opengradient_action_provider()
    args = {
        "contract_address" : "0xffffffffffffffffffffffffffffffffffffffff"
    }
    error_result = provider.read_workflow(args)
    assert "Error reading workflow" in error_result

@pytest.mark.usefixtures("mock_env")
def test_successful_read_workflow_action():
    """Test that read workflow returns the expected result from the SDK."""
    workflow_result = og.read_workflow_result(contract_address=BTC_FORECAST_ADDRESS)
    expected_result = str(workflow_result.numbers["Y"][0])

    provider = opengradient_action_provider()
    args = {
        "contract_address" : BTC_FORECAST_ADDRESS
    }
    result = provider.read_workflow(args)
    
    # Numpy cuts off accuracy to 8 decimals when converting to string
    assert expected_result[:10] in result
