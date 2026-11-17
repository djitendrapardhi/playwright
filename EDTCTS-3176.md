# EDTCTS-3176 — Knowledge Search Phase 2

**Story:** EDTCTS-3176  
**Subject:** Search from the article page within the same article's categories  
**Source:** `EDTCTS-3176.xlsx`  
**Environment:** `https://adt--test3.sandbox.my.site.com/help`

---

## Automation note

Manual Steps 2–6 (Salesforce login → Setup → All Sites → copy URL) are replaced by direct navigation to the Experience Cloud URL from the test case.

**Needs Clarification:** ADT Help User login is not used in automation because the Help site is publicly reachable. Provide env-based credentials if gated content is required.

---

## Test cases

| ID | Title | Priority focus |
|----|--------|----------------|
| TC_01 | Article appears once and Search field appears on the article page | Unique labels; Search on article |
| TC_02 | Single-category global results and suggestions | Category-scoped search URL |
| TC_03 | Article matches two or more metadata categories | `category=A%2CB` in URL |
| TC_04 | Article doesn’t belong to any metadata category | No `category` query param |

### TC_01 — Article appears once + Search on article page

**Preconditions:** Experience Cloud site active; keyword present in article labels.

| Step | Action | Expected |
|------|--------|----------|
| 1 | Open Help home | Heading **ADT Home Security Support Center**; Search visible |
| 2 | Enter keyword `ADT` and click Search | Results list loads with result count |
| 3 | Validate result titles | Each article label appears **once** |
| 4 | Open any article | Article detail loads |
| 5 | Validate Search | Knowledge Search field visible and enabled |

### TC_02 — Single-category global results

| Step | Action | Expected |
|------|--------|----------|
| 1 | Search `ADT` from home | Global results load (no category param) |
| 2 | Open category **ADT smart home security** | Category home + Search visible |
| 3 | Search `ADT` again | URL contains `category=ADT_smart_home_security` |
| 4 | Open categorized article | Article + Search visible |
| 5 | Search `ADT` from article | Results still limited to that category |

### TC_03 — Multi-category article

| Step | Action | Expected |
|------|--------|----------|
| 1 | Search `ADT` and open **Second ADT article in Smart home security and Pulse** | Article + Search visible |
| 2 | Search `ADT` from article | One `category` param with developer names separated by `,` / `%2C` (e.g. `ADT_smart_home_security%2CPulse`) |

### TC_04 — No metadata category

| Step | Action | Expected |
|------|--------|----------|
| 1 | Search `ADT` and open **ADT article NO category** | Article + Search visible |
| 2 | Search `ADT` from article | Results across categories; URL has **no** `category` parameter |

---

## Test data (sandbox)

| Key | Value |
|-----|--------|
| Help URL | `https://adt--test3.sandbox.my.site.com/help` |
| Keyword | `ADT` |
| Category path | `adtsmarthomesecurity` |
| Category API name | `ADT_smart_home_security` |
| Multi-category article | Second ADT article in Smart home security and Pulse |
| No-category article | ADT article NO category |
| Single-category article | ADT Smart Home Security- Arming Your System |

---

## How to run

### TypeScript (`@playwright/test`)

```powershell
cd C:\Users\v_djitendrapardhi\.cursor\Devesh\Playwright
npm init -y
npm install -D @playwright/test
npx playwright install chromium
npx playwright test tests/edtcts-3176.spec.ts --headed
```

### Python (existing suite)

```powershell
cd C:\Users\v_djitendrapardhi\.cursor\Devesh\Playwright
$env:PYTHONPATH = (Get-Location).Path
python -m pytest tests/test_edtcts_3176.py --browser chromium --headed -v
```

---

## Traceability

`EDTCTS-3176` → Manual TC_01–TC_04 → `tests/edtcts-3176.spec.ts` / `tests/test_edtcts_3176.py`
