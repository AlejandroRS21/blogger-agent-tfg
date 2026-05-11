import json
from unittest.mock import patch
import batch_generate as bg

def test_batch_generate_state_recovery(tmp_path):
    # Mock inputs
    input_file = tmp_path / "inputs.json"
    input_file.write_text(json.dumps({"topics": ["Topic A", "Topic B", "Topic C"]}))
    
    # Mock status json where Topic A is already completed
    status_file = tmp_path / "batch_status.json"
    status_file.write_text(json.dumps({
        "Topic A": {"success": True, "output_file": "path/a.json"},
        "Topic B": {"success": False, "error": "failed"} 
    }))
    
    out_dir = tmp_path / "out"
    out_dir.mkdir()

    with patch("batch_generate.INPUT_JSON", input_file), \
         patch("batch_generate.BATCH_STATUS_JSON", status_file), \
         patch("batch_generate.OUTPUT_DIR", out_dir), \
         patch("batch_generate.generate_single_post") as mock_generate, \
         patch("sys.argv", ["batch_generate.py", "--input", str(input_file), "--output", str(out_dir), "--urls", "https://javipas.com/test-1", "https://javipas.com/test-2"]):
         
        mock_generate.return_value = {"metadata": {"tokens": 100}}
        bg.main()
        
        # It should skip Topic A, retry Topic B, and run Topic C
        assert mock_generate.call_count == 2
        calls = [c[0][0] for c in mock_generate.call_args_list]
        assert "Topic B" in calls
        assert "Topic C" in calls

