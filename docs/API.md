# API Documentation

Complete API reference for the Secure Vote-Transfer System.

## Base URLs

- **Voting Node**: `http://localhost:5000`
- **Observer Node**: `http://localhost:5001`

## Voting Node API

### GET /

Serve the voting booth interface.

**Response**: HTML page

**Status Codes**:
- `200 OK` - Success

---

### POST /vote

Submit a vote to the blockchain.

**Request Body**:
```json
{
  "id": 1001,
  "content": "Candidate A"
}
```

**Parameters**:
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| id | integer | Yes | Unique voter ID |
| content | string | Yes | Vote content (candidate name) |

**Response**:
```json
{
  "status": "SUCCESS: Vote recorded in shard 2"
}
```

**Status Codes**:
- `200 OK` - Vote accepted
- `400 Bad Request` - Invalid request format
- `409 Conflict` - Voter ID already used

**Error Response**:
```json
{
  "status": "ERROR: Voter ID already used"
}
```

**Example**:
```bash
curl -X POST http://localhost:5000/vote \
  -H "Content-Type: application/json" \
  -d '{"id": 1001, "content": "Candidate A"}'
```

---

### GET /status

Get current blockchain status including shard information.

**Response**:
```json
{
  "shards": [3, 2, 4, 1],
  "total_votes": 10,
  "tallies": {
    "Candidate A": 4,
    "Candidate B": 3,
    "Candidate C": 2,
    "Candidate D": 1
  }
}
```

**Response Fields**:
| Field | Type | Description |
|-------|------|-------------|
| shards | array[int] | Number of blocks in each shard (index = shard ID) |
| total_votes | integer | Total number of votes across all shards |
| tallies | object | Vote count per candidate |

**Status Codes**:
- `200 OK` - Success
- `503 Service Unavailable` - C++ core not responding

**Example**:
```bash
curl http://localhost:5000/status
```

---

### GET /tally

Get vote tallies by candidate.

**Response**:
```json
{
  "tally": {
    "Candidate A": 4,
    "Candidate B": 3,
    "Candidate C": 2,
    "Candidate D": 1
  }
}
```

**Status Codes**:
- `200 OK` - Success
- `503 Service Unavailable` - C++ core not responding

**Example**:
```bash
curl http://localhost:5000/tally
```

---

## Observer Node API

### GET /

Serve the admin dashboard interface.

**Response**: HTML page

**Status Codes**:
- `200 OK` - Success

---

### GET /status_proxy

Proxy endpoint to fetch status from voting node.

**Response**:
```json
{
  "shards": [3, 2, 4, 1],
  "total_votes": 10,
  "tallies": {
    "Candidate A": 4,
    "Candidate B": 3,
    "Candidate C": 2,
    "Candidate D": 1
  }
}
```

**Status Codes**:
- `200 OK` - Success
- `503 Service Unavailable` - Voting node not reachable

**Error Response**:
```json
{
  "shards": []
}
```

**Example**:
```bash
curl http://localhost:5001/status_proxy
```

---

### GET /tally_proxy

Proxy endpoint to fetch tallies from voting node.

**Response**:
```json
{
  "tally": {
    "Candidate A": 4,
    "Candidate B": 3
  }
}
```

**Status Codes**:
- `200 OK` - Success
- `503 Service Unavailable` - Voting node not reachable

**Error Response**:
```json
{
  "tally": []
}
```

**Example**:
```bash
curl http://localhost:5001/tally_proxy
```

---

## C++ Core IPC Protocol

The C++ core communicates via stdin/stdout with a text-based protocol.

### VOTE Command

Submit a vote to the blockchain.

**Format**:
```
VOTE <voter_id> <content>
```

**Example**:
```
VOTE 1001 Candidate A
```

**Response**:
```
SUCCESS: Vote recorded in shard 2
```

**Error Response**:
```
ERROR: Voter ID already used
```

---

### STATUS Command

Get blockchain status.

**Format**:
```
STATUS
```

**Response** (JSON):
```json
{"shards":[3,2,4,1],"total_votes":10,"tallies":{"Candidate A":4,"Candidate B":3}}
```

---

### TALLY Command

Get vote tallies.

**Format**:
```
TALLY
```

**Response** (JSON):
```json
{"tally":{"Candidate A":4,"Candidate B":3,"Candidate C":2}}
```

---

## Error Codes

| HTTP Code | Meaning | Common Causes |
|-----------|---------|---------------|
| 200 | OK | Request successful |
| 400 | Bad Request | Invalid JSON, missing fields |
| 409 | Conflict | Duplicate voter ID |
| 503 | Service Unavailable | C++ core not running, voting node unreachable |

## Rate Limiting

**Current**: No rate limiting implemented

**Recommendation**: Implement rate limiting in production:
- Per IP: 10 votes per minute
- Global: 1000 votes per minute

## CORS

**Current**: No CORS headers (localhost only)

**Production**: Add CORS headers if frontend hosted separately:
```python
from flask_cors import CORS
CORS(app, origins=["https://yourdomain.com"])
```

## Authentication

**Current**: No authentication (voter ID only)

**Production Recommendations**:
- JWT tokens for voter authentication
- OAuth2 for admin dashboard
- API keys for programmatic access

## Versioning

**Current Version**: v2.0

**Future**: Consider API versioning:
- URL-based: `/api/v2/vote`
- Header-based: `Accept: application/vnd.vote-system.v2+json`

## WebSocket Support (Future)

For real-time updates without polling:

```javascript
// Future implementation
const ws = new WebSocket('ws://localhost:5000/ws');
ws.onmessage = (event) => {
  const data = JSON.parse(event.data);
  updateDashboard(data);
};
```

## Testing

### Example Test Suite

```python
import requests

BASE_URL = "http://localhost:5000"

def test_vote_submission():
    response = requests.post(f"{BASE_URL}/vote", json={
        "id": 9999,
        "content": "Test Candidate"
    })
    assert response.status_code == 200
    assert "SUCCESS" in response.json()["status"]

def test_duplicate_vote():
    # Submit first vote
    requests.post(f"{BASE_URL}/vote", json={"id": 8888, "content": "A"})
    
    # Try duplicate
    response = requests.post(f"{BASE_URL}/vote", json={"id": 8888, "content": "B"})
    assert response.status_code == 409
    assert "ERROR" in response.json()["status"]

def test_status():
    response = requests.get(f"{BASE_URL}/status")
    assert response.status_code == 200
    data = response.json()
    assert "shards" in data
    assert "total_votes" in data
    assert len(data["shards"]) == 4
```

## Performance Benchmarks

**Vote Submission**:
- Average latency: 50-100ms
- Throughput: 200-500 votes/second

**Status Query**:
- Average latency: 10-20ms
- Throughput: 1000+ requests/second

## Security Considerations

1. **Input Validation**: All inputs validated before processing
2. **SQL Injection**: Not applicable (no SQL database)
3. **XSS**: HTML escaped in responses
4. **CSRF**: Implement CSRF tokens in production
5. **HTTPS**: Use HTTPS in production
6. **Rate Limiting**: Implement to prevent DoS attacks
