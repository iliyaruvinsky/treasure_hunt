# File Upload Fixes

## Issues Fixed

### 1. Large File Upload Failures
**Problem:** Files larger than ~1MB were failing with JSON serialization errors (`NaN` values, out of range floats).

**Fixes Applied:**
- ✅ Added NaN/Infinity cleaning in `data_saver.py` - converts all NaN/Inf values to `null` before JSON serialization
- ✅ Added NaN handling in all parsers (`excel_parser_soda.py`, `excel_parser_4c.py`, `csv_parser.py`) - replaces NaN with None before converting to dict
- ✅ Enhanced JSON cleaning to handle numpy/pandas types, very large numbers, and non-serializable types
- ✅ Added file size limit configuration (100MB) in upload endpoint

### 2. Dashboard Not Showing Results
**Problem:** Small files uploaded successfully but findings didn't appear in dashboard.

**Fixes Applied:**
- ✅ Fixed upload response handling - correctly extracts `data_source_id` from response
- ✅ Added better error handling and logging in upload flow
- ✅ Added automatic query invalidation after analysis completes
- ✅ Added delay before navigation to allow data to be available

## Testing

### To Test Large File Upload:
1. Upload a file larger than 1MB
2. Check browser console for any errors
3. Verify file is saved and parsed successfully
4. Check backend logs: `docker compose logs backend`

### To Test Dashboard Display:
1. Upload a small file (< 1MB)
2. Wait for "Upload successful" message
3. Check browser console for "Analysis completed" message
4. Dashboard should automatically refresh and show findings
5. If no findings appear, check:
   - Browser console for errors
   - Backend logs for analysis errors
   - Database: `docker compose exec backend python -c "from app.core.database import SessionLocal; from app.models.finding import Finding; db = SessionLocal(); print(f'Findings: {db.query(Finding).count()}')"`

## Known Limitations

- File size limit: Currently configured for 100MB. Can be increased if needed.
- Analysis runs automatically after upload - if it fails, check backend logs
- Large files may take time to process - be patient

## Troubleshooting

### Upload fails with 400 error:
- Check file format is supported (PDF, CSV, DOCX, XLSX)
- Check file isn't corrupted
- Check backend logs for specific error

### Upload succeeds but no findings:
- Check if analysis ran: `docker compose logs backend | grep -i analysis`
- Manually trigger analysis via API: `POST /api/v1/analysis/run` with `{"data_source_id": <id>}`
- Check database for findings: See testing commands above

### Large file upload fails:
- Check backend logs for memory errors
- Consider increasing Docker memory limits
- File might be too large - try splitting into smaller files

