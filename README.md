# BryanNet API Reference

Version 1.0.0 -- generated from the live FastAPI OpenAPI schema.

Base URL (local development): `http://127.0.0.1:8000/api/v1`

## Authentication

Most endpoints require a bearer JWT obtained from `POST /auth/login`:

```
Authorization: Bearer <token>
```

The token is tied to a specific admin session row (`admin_sessions`). Closing that session (logout, forced close-all, or replacement by a new login) invalidates the token immediately, even if the JWT itself has not expired. Tokens expire after `JWT_EXPIRE_MINUTES` (default 1440 minutes / 24 hours).

A handful of endpoints are deliberately **not authenticated** because the Telegram bot calls them before a customer has any credentials -- onboarding start/name/phone, customer/plan/subscription-status lookups used by the bot, the session state-machine endpoint, and health checks. These are called out individually below.

## Error format

Every error response (raised via `HTTPException` or the global handlers) shares one envelope:

```json
{
  "success": false,
  "message": "Human-readable description of what went wrong."
}
```

Validation errors (`422`) add an `errors` array with Pydantic's field-level validation detail:

```json
{
  "success": false,
  "message": "Validation failed.",
  "errors": [ { "loc": [...], "msg": "...", "type": "..." } ]
}
```

Unhandled server errors return `500` with `{"success": false, "message": "An unexpected error occurred."}`.

## Pagination

List endpoints that support pagination accept `page` (>= 1, default 1) and `page_size` (1-100, default 25) query parameters and return:

```json
{
  "items": [...],
  "total": 0,
  "page": 1,
  "page_size": 25,
  "pages": 0
}
```

## Rate limits

| Endpoint | Limit |
|---|---|
| `POST /auth/login` | 5/minute per IP |
| `POST /automation/*` | 10/minute per IP |
| `POST /subscriptions/process` | 10/minute per IP |
| `GET /session/telegram/{telegram_user_id}` | 30/minute per IP |

Exceeding a limit returns `429 Too Many Requests`.

## Table of Contents

- [Enum Reference](#enum-reference)
- [Authentication](#authentication)
- [Administration](#administration)
- [Admin Sessions](#admin-sessions)
- [Dashboard](#dashboard)
- [Customers](#customers)
- [Plans](#plans)
- [Subscriptions](#subscriptions)
- [Devices](#devices)
- [Payments](#payments)
- [Automation](#automation)
- [Session](#session)
- [Health](#health)

## Enum Reference

Named enum types referenced throughout the schemas below.

| Enum | Values |
|---|---|
| `DeviceStatus` | `active`, `inactive`, `blocked` |
| `LoginSource` | `WEB`, `TELEGRAM`, `API` |
| `LogoutReason` | `MANUAL`, `CLOSE_ALL`, `NEW_LOGIN`, `TOKEN_EXPIRED` |
| `NextAction` | `START_ONBOARDING`, `ENTER_NAME`, `ENTER_PHONE_NUMBER`, `COMPLETE`, `SHOW_MAIN_MENU` |
| `PaymentChannel` | `cash`, `bank_transfer`, `card`, `ussd`, `wallet`, `system` |
| `PaymentProvider` | `paystack`, `flutterwave`, `monnify`, `manual` |
| `PaymentStatus` | `pending`, `successful`, `failed`, `cancelled`, `refunded`, `expired` |
| `SubscriptionStatus` | `queued`, `active`, `expired`, `cancelled` |


---

## Authentication

Admin login and current-session identity.

### Admin login

`POST /auth/login`

No authentication required.

Authenticates an administrator with username and password, creates a new admin session record, logs the login in the audit trail, and returns a JWT bearer token scoped to that session. Rate limited to 5 requests/minute per client IP.

**Request body**: `LoginRequest`

| Field | Type | Required | Notes |
|---|---|---|---|
| `username` | string | yes | minLength: 3; maxLength: 50 |
| `password` | string | yes | minLength: 8; maxLength: 255 |

**Responses**

- `200 OK` Returns `LoginResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `429 Too Many Requests` -- Too many requests -- rate limit exceeded.

<details><summary><code>LoginResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `access_token` | string | yes |  |
| `token_type` | string | no | default `bearer` |

</details>


### Get current admin

`GET /auth/me`

**Requires** `Authorization: Bearer <token>`.

Returns the identity of the administrator associated with the current bearer token.

**Responses**

- `200 OK` Returns `CurrentAdminResponse`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.

<details><summary><code>CurrentAdminResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `admin_user_id` | integer | yes |  |
| `username` | string | yes |  |
| `email` | string | yes |  |
| `role` | string | yes |  |
| `is_active` | boolean | yes |  |

</details>



---

## Administration

Aggregated administration overview: metrics, recent audit logs, active sessions, system activity.

### Administration overview

`GET /administration/overview`

**Requires** `Authorization: Bearer <token>`.

Returns a combined snapshot for the administration screen: headline metrics (admin user count, active sessions, roles, audit/system events today), the most recent audit log entries, currently active sessions, and recent system activity.

**Responses**

- `200 OK` Returns `AdministrationOverviewResponse`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `403 Forbidden` -- Admin account is inactive.

<details><summary><code>AdministrationOverviewResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `metrics` | AdministrationMetrics | yes |  |
| `recent_audit_logs` | array[RecentAuditLogItem] | yes |  |
| `active_sessions` | array[ActiveSessionItem] | yes |  |
| `system_activity` | array[SystemActivityItem] | yes |  |

</details>



---

## Admin Sessions

Admin login session lifecycle: activity tracking, closing sessions, session queries.

### Touch session activity

`PATCH /admin-sessions/{admin_session_id}/activity`

**Requires** `Authorization: Bearer <token>`.

Updates the `last_activity` timestamp on an admin session. Used to keep a session alive.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `admin_session_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `AdminSessionResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Admin session not found.

<details><summary><code>AdminSessionResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `admin_session_id` | integer | yes |  |
| `admin_user_id` | integer | yes |  |
| `login_time` | string<date-time> | yes |  |
| `last_activity` | string<date-time> | yes |  |
| `logout_time` | string<date-time> (nullable) | yes |  |
| `ip_address` | string (nullable) | yes |  |
| `user_agent` | string (nullable) | yes |  |
| `login_source` | LoginSource | yes |  |
| `client_name` | string | yes |  |
| `logout_reason` | LogoutReason (nullable) | yes |  |
| `is_active` | boolean | yes |  |

</details>


### Close a session

`PATCH /admin-sessions/{admin_session_id}/close`

**Requires** `Authorization: Bearer <token>`.

Manually closes a single admin session (logout). Sets `is_active` to false and records a logout reason and time.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `admin_session_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `AdminSessionResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Admin session not found.

<details><summary><code>AdminSessionResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `admin_session_id` | integer | yes |  |
| `admin_user_id` | integer | yes |  |
| `login_time` | string<date-time> | yes |  |
| `last_activity` | string<date-time> | yes |  |
| `logout_time` | string<date-time> (nullable) | yes |  |
| `ip_address` | string (nullable) | yes |  |
| `user_agent` | string (nullable) | yes |  |
| `login_source` | LoginSource | yes |  |
| `client_name` | string | yes |  |
| `logout_reason` | LogoutReason (nullable) | yes |  |
| `is_active` | boolean | yes |  |

</details>


### Close all sessions for an admin

`PATCH /admin-sessions/close-all/{admin_user_id}`

**Requires** `Authorization: Bearer <token>`.

Closes every active session belonging to the given admin user, e.g. when forcing a logout everywhere. Returns the number of sessions closed.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `admin_user_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `JobResultResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.

<details><summary><code>JobResultResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `processed` | integer | yes |  |
| `message` | string | yes |  |

</details>


### List admin sessions

`GET /admin-sessions/`

No authentication required.

Returns admin sessions with optional filters by admin user and active status, sortable and paginated (`page`, `page_size` query params). Note: this endpoint is not itself behind `get_current_admin`, but is intended for authenticated dashboard use.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `admin_user_id` | query | integer (nullable) | no | -- |
| `is_active` | query | boolean (nullable) | no | -- |
| `sort_by` | query | string | no | login_time |
| `sort_order` | query | string | no | desc |
| `page` | query | integer | no | 1 |
| `page_size` | query | integer | no | 25 |

**Responses**

- `200 OK` Returns `AdminSessionResponse (array)`.
- `422 Validation Error` -- Request body or query parameters failed validation.


### List active sessions

`GET /admin-sessions/active`

**Requires** `Authorization: Bearer <token>`.

Returns all currently active admin sessions across all administrators.

**Responses**

- `200 OK` Returns `AdminSessionResponse (array)`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.


### Get a session

`GET /admin-sessions/{admin_session_id}`

**Requires** `Authorization: Bearer <token>`.

Returns a single admin session by its ID.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `admin_session_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `AdminSessionResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Admin session not found.

<details><summary><code>AdminSessionResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `admin_session_id` | integer | yes |  |
| `admin_user_id` | integer | yes |  |
| `login_time` | string<date-time> | yes |  |
| `last_activity` | string<date-time> | yes |  |
| `logout_time` | string<date-time> (nullable) | yes |  |
| `ip_address` | string (nullable) | yes |  |
| `user_agent` | string (nullable) | yes |  |
| `login_source` | LoginSource | yes |  |
| `client_name` | string | yes |  |
| `logout_reason` | LogoutReason (nullable) | yes |  |
| `is_active` | boolean | yes |  |

</details>


### List sessions for an admin

`GET /admin-sessions/admin/{admin_user_id}`

**Requires** `Authorization: Bearer <token>`.

Returns the full session history for a given admin user.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `admin_user_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `AdminSessionResponse (array)`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.


### Get an admin's active session

`GET /admin-sessions/admin/{admin_user_id}/active`

**Requires** `Authorization: Bearer <token>`.

Returns the single currently active session for an admin user, or `null` if none.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `admin_user_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `AdminSessionResponse (nullable)`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.



---

## Dashboard

Business metrics for the admin dashboard: revenue, subscriptions, recent activity.

### Dashboard summary

`GET /dashboard/summary`

**Requires** `Authorization: Bearer <token>`.

Headline numbers for the admin dashboard: customers, active/queued subscriptions, active devices, revenue totals, revenue today, subscriptions expiring today/next 7 days, and new customers today/this month.

**Responses**

- `200 OK` Returns `DashboardSummaryResponse`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `403 Forbidden` -- Admin account is inactive.

<details><summary><code>DashboardSummaryResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `total_customers` | integer | yes |  |
| `active_subscriptions` | integer | yes |  |
| `queued_subscriptions` | integer | yes |  |
| `active_devices` | integer | yes |  |
| `total_revenue` | number | yes |  |
| `total_payments` | integer | yes |  |
| `revenue_today` | number | yes |  |
| `expiring_today` | integer | yes |  |
| `expiring_next_7_days` | integer | yes |  |
| `new_customers_today` | integer | yes |  |
| `new_customers_this_month` | integer | yes |  |

</details>


### Revenue overview

`GET /dashboard/revenue-overview`

**Requires** `Authorization: Bearer <token>`.

Revenue broken down over a time window. `period` accepts `7d`, `30d`, `month`, or `12m` (default `month`); the response is a list of labeled buckets with revenue totals.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `period` | query | string | no | month |

**Responses**

- `200 OK` Returns `RevenueOverviewItem (array)`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `403 Forbidden` -- Admin account is inactive.


### Subscription status breakdown

`GET /dashboard/subscription-breakdown`

**Requires** `Authorization: Bearer <token>`.

Returns a count of subscriptions grouped by status (queued, active, expired, cancelled).

**Responses**

- `200 OK` Returns `SubscriptionBreakdownItem (array)`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `403 Forbidden` -- Admin account is inactive.


### Recent activity feed

`GET /dashboard/recent-activity`

**Requires** `Authorization: Bearer <token>`.

Returns the most recent notable events across the platform (payments, subscriptions, etc.), newest first. `limit` controls how many are returned (default 10).

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `limit` | query | integer | no | 10 |

**Responses**

- `200 OK` Returns `RecentActivityItem (array)`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `403 Forbidden` -- Admin account is inactive.



---

## Customers

Customer identity, registration, and the Telegram onboarding flow.

### Register a customer (admin)

`POST /customers/register`

**Requires** `Authorization: Bearer <token>`.

Creates a customer record directly from the admin dashboard, bypassing the Telegram onboarding flow. Phone number must be unique.

**Request body**: `CustomerCreate`

| Field | Type | Required | Notes |
|---|---|---|---|
| `phone_number` | string | yes | minLength: 11; maxLength: 15; pattern: ^\+?[0-9]+$ |
| `full_name` | string | yes | minLength: 3; maxLength: 100 |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `400 Bad Request` -- Customer with this phone number already exists.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>


### Update a customer

`PUT /customers/{customer_id}`

**Requires** `Authorization: Bearer <token>`.

Updates a customer's phone number and full name.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Request body**: `CustomerUpdate`

| Field | Type | Required | Notes |
|---|---|---|---|
| `phone_number` | string | yes | minLength: 11; maxLength: 15; pattern: ^\+?[0-9]+$ |
| `full_name` | string | yes | minLength: 3; maxLength: 100 |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Customer not found.
- `400 Bad Request` -- Customer with this phone number already exists.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>


### Activate a customer

`PATCH /customers/{customer_id}/activate`

**Requires** `Authorization: Bearer <token>`.

Marks a customer account as active.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Customer not found.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>


### Deactivate a customer

`PATCH /customers/{customer_id}/deactivate`

**Requires** `Authorization: Bearer <token>`.

Marks a customer account as inactive.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Customer not found.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>


### Start Telegram onboarding

`POST /customers/onboarding/start`

No authentication required.

Called by the Telegram bot the first time a Telegram user interacts with it. Creates a bare customer record keyed by `telegram_user_id` with registration in progress. Not authenticated -- it is the very first touchpoint before any credentials exist.

**Request body**: `CustomerOnboardingStart`

| Field | Type | Required | Notes |
|---|---|---|---|
| `telegram_user_id` | integer | yes | exclusiveMinimum: 0.0 |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>


### Set name during onboarding

`PATCH /customers/onboarding/name`

No authentication required.

Sets the customer's full name during the Telegram onboarding flow, identified by `telegram_user_id`. Not authenticated.

**Request body**: `CustomerUpdateName`

| Field | Type | Required | Notes |
|---|---|---|---|
| `telegram_user_id` | integer | yes | exclusiveMinimum: 0.0 |
| `full_name` | string | yes | minLength: 3; maxLength: 100 |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `404 Not Found` -- Customer not found.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>


### Set phone during onboarding

`PATCH /customers/onboarding/phone`

No authentication required.

Sets the customer's phone number during the Telegram onboarding flow, identified by `telegram_user_id`. Phone number must be unique. Not authenticated.

**Request body**: `CustomerUpdatePhone`

| Field | Type | Required | Notes |
|---|---|---|---|
| `telegram_user_id` | integer | yes | exclusiveMinimum: 0.0 |
| `phone_number` | string | yes | minLength: 11; maxLength: 15; pattern: ^\+?[0-9]+$ |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `404 Not Found` -- Customer not found.
- `400 Bad Request` -- Customer with this phone number already exists.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>


### List customers

`GET /customers/`

No authentication required.

Paginated, searchable, sortable list of customers for the admin dashboard. Note: unlike other customer endpoints, this route does not require `get_current_admin` in the current code.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `search` | query | string (nullable) | no | -- |
| `sort_by` | query | string | no | customer_id |
| `sort_order` | query | string | no | asc |
| `page` | query | integer | no | 1 |
| `page_size` | query | integer | no | 25 |

**Responses**

- `200 OK` Returns `PaginatedResponse_CustomerListItem_`.
- `422 Validation Error` -- Request body or query parameters failed validation.

<details><summary><code>PaginatedResponse_CustomerListItem_</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `items` | array[CustomerListItem] | yes |  |
| `total` | integer | yes |  |
| `page` | integer | yes |  |
| `page_size` | integer | yes |  |
| `pages` | integer | yes |  |

</details>


### Get customer by ID

`GET /customers/id/{customer_id}`

**Requires** `Authorization: Bearer <token>`.

Returns a single customer by internal ID.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Customer not found.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>


### Get customer by phone

`GET /customers/phone/{phone_number}`

**Requires** `Authorization: Bearer <token>`.

Looks up a customer by phone number.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `phone_number` | path | string | yes | -- |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Customer not found.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>


### Get customer by Telegram ID

`GET /customers/telegram/{telegram_user_id}`

No authentication required.

Looks up a customer by their Telegram user ID. Used by the bot to resume a known customer's session. Not authenticated.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `telegram_user_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `CustomerResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `404 Not Found` -- Customer not found.

<details><summary><code>CustomerResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `phone_number` | string (nullable) | no |  |
| `full_name` | string (nullable) | no |  |
| `telegram_user_id` | integer (nullable) | no |  |
| `is_registered` | boolean | yes |  |
| `registration_step` | string | yes |  |

</details>



---

## Plans

Internet plan catalog: pricing, speed, duration, device limits.

### Create a plan

`POST /plans/`

**Requires** `Authorization: Bearer <token>`.

Creates a new internet plan. Plan names must be unique.

**Request body**: `PlanCreate`

| Field | Type | Required | Notes |
|---|---|---|---|
| `plan_name` | string | yes | minLength: 2; maxLength: 100 |
| `price` | number or string | yes |  |
| `duration_days` | number | yes | exclusiveMinimum: 0.0 |
| `speed_limit_mbps` | integer | yes | exclusiveMinimum: 0.0 |
| `max_devices` | integer | yes | exclusiveMinimum: 0.0 |
| `concurrent_devices` | integer | yes | exclusiveMinimum: 0.0 |
| `is_active` | boolean | no | default `True` |

**Responses**

- `201 Created` Returns `PlanResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `400 Bad Request` -- A plan with this name already exists.

<details><summary><code>PlanResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `plan_id` | integer | yes |  |
| `plan_name` | string | yes |  |
| `price` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `duration_days` | number | yes | exclusiveMinimum: 0.0 |
| `speed_limit_mbps` | integer | yes |  |
| `max_devices` | integer | yes |  |
| `concurrent_devices` | integer | yes |  |
| `is_active` | boolean | yes |  |

</details>


### List plans

`GET /plans/`

No authentication required.

Returns all plans (paginated), including inactive ones. Not authenticated -- used by the bot's plan picker.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `page` | query | integer | no | 1 |
| `page_size` | query | integer | no | 25 |

**Responses**

- `200 OK` Returns `PlanResponse (array)`.
- `422 Validation Error` -- Request body or query parameters failed validation.


### Update a plan

`PUT /plans/{plan_id}`

**Requires** `Authorization: Bearer <token>`.

Replaces a plan's commercial details (price, duration, speed, device limits).

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `plan_id` | path | integer | yes | -- |

**Request body**: `PlanCreate`

| Field | Type | Required | Notes |
|---|---|---|---|
| `plan_name` | string | yes | minLength: 2; maxLength: 100 |
| `price` | number or string | yes |  |
| `duration_days` | number | yes | exclusiveMinimum: 0.0 |
| `speed_limit_mbps` | integer | yes | exclusiveMinimum: 0.0 |
| `max_devices` | integer | yes | exclusiveMinimum: 0.0 |
| `concurrent_devices` | integer | yes | exclusiveMinimum: 0.0 |
| `is_active` | boolean | no | default `True` |

**Responses**

- `200 OK` Returns `PlanResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Plan not found.
- `400 Bad Request` -- A plan with this name already exists.

<details><summary><code>PlanResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `plan_id` | integer | yes |  |
| `plan_name` | string | yes |  |
| `price` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `duration_days` | number | yes | exclusiveMinimum: 0.0 |
| `speed_limit_mbps` | integer | yes |  |
| `max_devices` | integer | yes |  |
| `concurrent_devices` | integer | yes |  |
| `is_active` | boolean | yes |  |

</details>


### Get a plan

`GET /plans/{plan_id}`

**Requires** `Authorization: Bearer <token>`.

Returns a single plan by ID.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `plan_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `PlanResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Plan not found.

<details><summary><code>PlanResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `plan_id` | integer | yes |  |
| `plan_name` | string | yes |  |
| `price` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `duration_days` | number | yes | exclusiveMinimum: 0.0 |
| `speed_limit_mbps` | integer | yes |  |
| `max_devices` | integer | yes |  |
| `concurrent_devices` | integer | yes |  |
| `is_active` | boolean | yes |  |

</details>


### Activate a plan

`PATCH /plans/{plan_id}/activate`

**Requires** `Authorization: Bearer <token>`.

Marks a plan as active and available for purchase.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `plan_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `PlanResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Plan not found.

<details><summary><code>PlanResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `plan_id` | integer | yes |  |
| `plan_name` | string | yes |  |
| `price` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `duration_days` | number | yes | exclusiveMinimum: 0.0 |
| `speed_limit_mbps` | integer | yes |  |
| `max_devices` | integer | yes |  |
| `concurrent_devices` | integer | yes |  |
| `is_active` | boolean | yes |  |

</details>


### Deactivate a plan

`PATCH /plans/{plan_id}/deactivate`

**Requires** `Authorization: Bearer <token>`.

Marks a plan as inactive; it stops appearing in active-plan listings but existing subscriptions are unaffected.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `plan_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `PlanResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Plan not found.

<details><summary><code>PlanResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `plan_id` | integer | yes |  |
| `plan_name` | string | yes |  |
| `price` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `duration_days` | number | yes | exclusiveMinimum: 0.0 |
| `speed_limit_mbps` | integer | yes |  |
| `max_devices` | integer | yes |  |
| `concurrent_devices` | integer | yes |  |
| `is_active` | boolean | yes |  |

</details>


### List active plans

`GET /plans/active`

**Requires** `Authorization: Bearer <token>`.

Returns only plans currently marked active -- what a customer should be offered when purchasing. Not authenticated.

**Responses**

- `200 OK` Returns `PlanResponse (array)`.



---

## Subscriptions

Subscription lifecycle: purchase, queueing, cancellation, and status.

### Create a subscription

`POST /subscriptions/purchase`

**Requires** `Authorization: Bearer <token>`.

Creates a subscription for a customer/plan pair. If the customer has no active subscription, the new one starts immediately with status `active`. If the customer already has an active subscription, the new one is created with status `queued` and its start date is set to the current subscription's expiry -- it activates automatically when the current one expires. This is normally called internally by `PaymentService.complete_payment` once a payment is verified, but is also exposed directly for admin-assisted or manual subscription creation.

**Request body**: `SubscriptionPurchase`

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes | exclusiveMinimum: 0.0 |
| `plan_id` | integer | yes | exclusiveMinimum: 0.0 |

**Responses**

- `200 OK` Returns `SubscriptionResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Customer or plan not found.

<details><summary><code>SubscriptionResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `subscription_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `start_date` | string<date-time> | yes |  |
| `expiry_date` | string<date-time> | yes |  |
| `activation_sequence` | integer | yes |  |
| `status` | SubscriptionStatus | yes |  |
| `activated_at` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### Cancel a queued subscription

`PATCH /subscriptions/{subscription_id}/cancel`

**Requires** `Authorization: Bearer <token>`.

Cancels a subscription that is still `queued` (not yet active). Active or already-finished subscriptions cannot be cancelled this way.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `subscription_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `SubscriptionResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Subscription not found.
- `400 Bad Request` -- Only queued subscriptions can be cancelled.

<details><summary><code>SubscriptionResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `subscription_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `start_date` | string<date-time> | yes |  |
| `expiry_date` | string<date-time> | yes |  |
| `activation_sequence` | integer | yes |  |
| `status` | SubscriptionStatus | yes |  |
| `activated_at` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### Run subscription maintenance

`POST /subscriptions/process`

**Requires** `Authorization: Bearer <token>`.

Manually triggers the subscription background job (expiring due subscriptions, activating queued ones whose turn has come, etc.) and returns how many were processed. Rate limited to 10 requests/minute.

**Responses**

- `200 OK` Returns `JobResultResponse`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `429 Too Many Requests` -- Too many requests -- rate limit exceeded.

<details><summary><code>JobResultResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `processed` | integer | yes |  |
| `message` | string | yes |  |

</details>


### List subscriptions

`GET /subscriptions/`

No authentication required.

Paginated, filterable (customer, plan, status) list of subscriptions for the admin dashboard. Note: unlike other subscription endpoints, this route does not require `get_current_admin` in the current code.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | query | integer (nullable) | no | -- |
| `plan_id` | query | integer (nullable) | no | -- |
| `status` | query | SubscriptionStatus (nullable) | no | -- |
| `sort_by` | query | string | no | created_at |
| `sort_order` | query | string | no | desc |
| `page` | query | integer | no | 1 |
| `page_size` | query | integer | no | 25 |

**Responses**

- `200 OK` Returns `SubscriptionAdminResponse (array)`.
- `422 Validation Error` -- Request body or query parameters failed validation.


### Get a subscription

`GET /subscriptions/{subscription_id}`

**Requires** `Authorization: Bearer <token>`.

Returns a single subscription with admin-facing detail (customer name, plan name, remaining days).

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `subscription_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `SubscriptionAdminResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Subscription not found.

<details><summary><code>SubscriptionAdminResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `subscription_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `customer_name` | string | yes |  |
| `plan_id` | integer | yes |  |
| `plan_name` | string | yes |  |
| `price` | number | yes |  |
| `start_date` | string<date-time> | yes |  |
| `expiry_date` | string<date-time> | yes |  |
| `remaining_days` | integer | yes |  |
| `activation_sequence` | integer | yes |  |
| `status` | SubscriptionStatus | yes |  |
| `activated_at` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### List a customer's subscriptions

`GET /subscriptions/customer/{customer_id}`

**Requires** `Authorization: Bearer <token>`.

Returns every subscription (any status) belonging to a customer.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `SubscriptionAdminResponse (array)`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.


### Get a customer's active subscription

`GET /subscriptions/customer/{customer_id}/active`

**Requires** `Authorization: Bearer <token>`.

Returns the customer's current active subscription, if any.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `SubscriptionResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.

<details><summary><code>SubscriptionResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `subscription_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `start_date` | string<date-time> | yes |  |
| `expiry_date` | string<date-time> | yes |  |
| `activation_sequence` | integer | yes |  |
| `status` | SubscriptionStatus | yes |  |
| `activated_at` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### List a customer's queued subscriptions

`GET /subscriptions/customer/{customer_id}/queued`

**Requires** `Authorization: Bearer <token>`.

Returns subscriptions waiting to activate once the current active one expires.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `SubscriptionResponse (array)`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.


### Get a customer's subscription status

`GET /subscriptions/customer/{customer_id}/status`

No authentication required.

Lightweight status check used by the Telegram bot: whether the customer has an active subscription, the plan name and expiry if so, and how many subscriptions are queued behind it. Not authenticated.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `SubscriptionStatusResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.

<details><summary><code>SubscriptionStatusResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `has_active_subscription` | boolean | yes |  |
| `plan_name` | string (nullable) | no |  |
| `expiry_date` | string<date-time> (nullable) | no |  |
| `queued_subscriptions` | integer | yes |  |

</details>



---

## Devices

Customer devices: registration, approval, blocking, replacement.

### Register a device

`POST /devices/register`

**Requires** `Authorization: Bearer <token>`.

Registers a new device (MAC address) for a customer. The customer must have an active subscription, and must be under the plan's device limit. Duplicate MAC addresses for the same customer are rejected.

**Request body**: `DeviceCreate`

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes | exclusiveMinimum: 0.0 |
| `device_name` | string | yes | minLength: 2; maxLength: 100 |
| `mac_address` | string | yes | pattern: ^([0-9A-Fa-f]{2}:){5}[0-9A-Fa-f]{2}$ |

**Responses**

- `200 OK` Returns `DeviceResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `400 Bad Request` -- Customer has no active subscription / Device limit reached / Device already exists.
- `404 Not Found` -- Customer not found.

<details><summary><code>DeviceResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `device_name` | string | yes |  |
| `mac_address` | string | yes |  |
| `device_status` | DeviceStatus | yes |  |

</details>


### Activate a device

`PATCH /devices/{device_id}/activate`

**Requires** `Authorization: Bearer <token>`.

Activates a previously inactive device.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `device_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `DeviceResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Device not found.

<details><summary><code>DeviceResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `device_name` | string | yes |  |
| `mac_address` | string | yes |  |
| `device_status` | DeviceStatus | yes |  |

</details>


### Deactivate a device

`PATCH /devices/{device_id}/deactivate`

**Requires** `Authorization: Bearer <token>`.

Deactivates a device without blocking it outright.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `device_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `DeviceResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Device not found.

<details><summary><code>DeviceResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `device_name` | string | yes |  |
| `mac_address` | string | yes |  |
| `device_status` | DeviceStatus | yes |  |

</details>


### Approve a device

`PATCH /devices/{device_id}/approve`

**Requires** `Authorization: Bearer <token>`.

Marks a device as approved by the customer (e.g. confirming a new device is theirs).

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `device_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `DeviceResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Device not found.

<details><summary><code>DeviceResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `device_name` | string | yes |  |
| `mac_address` | string | yes |  |
| `device_status` | DeviceStatus | yes |  |

</details>


### Block a device

`PATCH /devices/{device_id}/block`

**Requires** `Authorization: Bearer <token>`.

Blocks a device from network access. A device that is already blocked cannot be blocked again.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `device_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `DeviceResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Device not found.
- `400 Bad Request` -- Device is already blocked.

<details><summary><code>DeviceResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `device_name` | string | yes |  |
| `mac_address` | string | yes |  |
| `device_status` | DeviceStatus | yes |  |

</details>


### Unblock a device

`PATCH /devices/{device_id}/unblock`

**Requires** `Authorization: Bearer <token>`.

Restores network access to a previously blocked device.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `device_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `DeviceResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Device not found.
- `400 Bad Request` -- Device is not blocked.

<details><summary><code>DeviceResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `device_name` | string | yes |  |
| `mac_address` | string | yes |  |
| `device_status` | DeviceStatus | yes |  |

</details>


### Rename a device

`PATCH /devices/{device_id}/rename`

**Requires** `Authorization: Bearer <token>`.

Updates a device's display name.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `device_id` | path | integer | yes | -- |

**Request body**: `DeviceRenameRequest`

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_name` | string | yes | minLength: 2; maxLength: 100 |

**Responses**

- `200 OK` Returns `DeviceResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Device not found.

<details><summary><code>DeviceResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `device_name` | string | yes |  |
| `mac_address` | string | yes |  |
| `device_status` | DeviceStatus | yes |  |

</details>


### Replace a device

`POST /devices/replace`

**Requires** `Authorization: Bearer <token>`.

Swaps one of a customer's devices for another (e.g. new phone). Both devices must belong to the specified customer.

**Request body**: `DeviceReplacementRequest`

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes | exclusiveMinimum: 0.0 |
| `old_device_id` | integer | yes | exclusiveMinimum: 0.0 |
| `new_device_id` | integer | yes | exclusiveMinimum: 0.0 |

**Responses**

- `200 OK` Returns `DeviceResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `400 Bad Request` -- Device does not belong to this customer.
- `404 Not Found` -- Customer or device not found.

<details><summary><code>DeviceResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `device_name` | string | yes |  |
| `mac_address` | string | yes |  |
| `device_status` | DeviceStatus | yes |  |

</details>


### List devices

`GET /devices/`

No authentication required.

Paginated, filterable (search, customer, status) list of devices. Note: unlike other device endpoints, this route does not require `get_current_admin` in the current code.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `search` | query | string (nullable) | no | -- |
| `customer_id` | query | integer (nullable) | no | -- |
| `device_status` | query | DeviceStatus (nullable) | no | -- |
| `sort_by` | query | string | no | device_id |
| `sort_order` | query | string | no | asc |
| `page` | query | integer | no | 1 |
| `page_size` | query | integer | no | 25 |

**Responses**

- `200 OK` Returns `PaginatedResponse_DeviceListItem_`.
- `422 Validation Error` -- Request body or query parameters failed validation.

<details><summary><code>PaginatedResponse_DeviceListItem_</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `items` | array[DeviceListItem] | yes |  |
| `total` | integer | yes |  |
| `page` | integer | yes |  |
| `page_size` | integer | yes |  |
| `pages` | integer | yes |  |

</details>


### Get a device

`GET /devices/{device_id}`

**Requires** `Authorization: Bearer <token>`.

Returns a single device by ID.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `device_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `DeviceResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Device not found.

<details><summary><code>DeviceResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `device_id` | integer | yes |  |
| `customer_id` | integer | yes |  |
| `device_name` | string | yes |  |
| `mac_address` | string | yes |  |
| `device_status` | DeviceStatus | yes |  |

</details>


### List a customer's devices

`GET /devices/customer/{customer_id}`

**Requires** `Authorization: Bearer <token>`.

Returns every device registered to a customer.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `DeviceResponse (array)`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.


### List a customer's active devices

`GET /devices/customer/{customer_id}/active`

**Requires** `Authorization: Bearer <token>`.

Returns only the customer's currently active devices.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `DeviceResponse (array)`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.



---

## Payments

Payment transactions: creation, completion, cancellation, refunds, expiry.

### Create a payment

`POST /payments/`

**Requires** `Authorization: Bearer <token>`.

Creates a pending payment transaction for a customer/plan pair via the given provider and channel. This does not grant any entitlement by itself -- it is completed separately once the provider confirms it.

**Request body**: `PaymentCreate`

| Field | Type | Required | Notes |
|---|---|---|---|
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `payment_provider` | PaymentProvider | yes |  |
| `payment_channel` | PaymentChannel | yes |  |
| `payment_method` | string | yes |  |

**Responses**

- `201 Created` Returns `PaymentResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Customer or plan not found.

<details><summary><code>PaymentResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `payment_reference` | string | yes |  |
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `subscription_id` | integer (nullable) | yes |  |
| `amount` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `payment_provider` | PaymentProvider | yes |  |
| `payment_method` | string (nullable) | yes |  |
| `gateway_transaction_id` | string (nullable) | yes |  |
| `status` | PaymentStatus | yes |  |
| `payment_date` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### List payments

`GET /payments/`

No authentication required.

Paginated, filterable (customer, provider, channel, method, status) list of payments. Note: unlike other payment endpoints, this route does not require `get_current_admin` in the current code.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | query | integer (nullable) | no | -- |
| `payment_provider` | query | PaymentProvider (nullable) | no | -- |
| `payment_channel` | query | PaymentChannel (nullable) | no | -- |
| `payment_method` | query | string (nullable) | no | -- |
| `status` | query | PaymentStatus (nullable) | no | -- |
| `sort_by` | query | string | no | created_at |
| `sort_order` | query | string | no | desc |
| `page` | query | integer | no | 1 |
| `page_size` | query | integer | no | 25 |

**Responses**

- `200 OK` Returns `PaginatedResponse_PaymentListItem_`.
- `422 Validation Error` -- Request body or query parameters failed validation.

<details><summary><code>PaginatedResponse_PaymentListItem_</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `items` | array[PaymentListItem] | yes |  |
| `total` | integer | yes |  |
| `page` | integer | yes |  |
| `page_size` | integer | yes |  |
| `pages` | integer | yes |  |

</details>


### Complete a payment

`POST /payments/{payment_reference}/complete`

**Requires** `Authorization: Bearer <token>`.

Marks a pending payment as successful and, in the same operation, creates the resulting subscription (via `SubscriptionService.create_subscription`) and links it back to the payment. Only pending payments can be completed.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `payment_reference` | path | string | yes | -- |
| `gateway_transaction_id` | query | string (nullable) | no | -- |

**Responses**

- `200 OK` Returns `PaymentResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Payment not found.
- `400 Bad Request` -- Only pending payments can be completed.

<details><summary><code>PaymentResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `payment_reference` | string | yes |  |
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `subscription_id` | integer (nullable) | yes |  |
| `amount` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `payment_provider` | PaymentProvider | yes |  |
| `payment_method` | string (nullable) | yes |  |
| `gateway_transaction_id` | string (nullable) | yes |  |
| `status` | PaymentStatus | yes |  |
| `payment_date` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### Cancel a payment

`PATCH /payments/{payment_reference}/cancel`

**Requires** `Authorization: Bearer <token>`.

Cancels a pending payment before it is completed. Only pending payments can be cancelled.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `payment_reference` | path | string | yes | -- |

**Responses**

- `200 OK` Returns `PaymentResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Payment not found.
- `400 Bad Request` -- Only pending payments can be cancelled.

<details><summary><code>PaymentResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `payment_reference` | string | yes |  |
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `subscription_id` | integer (nullable) | yes |  |
| `amount` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `payment_provider` | PaymentProvider | yes |  |
| `payment_method` | string (nullable) | yes |  |
| `gateway_transaction_id` | string (nullable) | yes |  |
| `status` | PaymentStatus | yes |  |
| `payment_date` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### Refund a payment

`PATCH /payments/{payment_reference}/refund`

**Requires** `Authorization: Bearer <token>`.

Marks a successful payment as refunded. Only successful payments can be refunded.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `payment_reference` | path | string | yes | -- |

**Responses**

- `200 OK` Returns `PaymentResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Payment not found.
- `400 Bad Request` -- Only successful payments can be refunded.

<details><summary><code>PaymentResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `payment_reference` | string | yes |  |
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `subscription_id` | integer (nullable) | yes |  |
| `amount` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `payment_provider` | PaymentProvider | yes |  |
| `payment_method` | string (nullable) | yes |  |
| `gateway_transaction_id` | string (nullable) | yes |  |
| `status` | PaymentStatus | yes |  |
| `payment_date` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### Expire a payment

`PATCH /payments/{payment_reference}/expire`

**Requires** `Authorization: Bearer <token>`.

Marks a pending payment as expired, e.g. after a provider callback window has passed. Only pending payments can be expired.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `payment_reference` | path | string | yes | -- |

**Responses**

- `200 OK` Returns `PaymentResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Payment not found.
- `400 Bad Request` -- Only pending payments can be expired.

<details><summary><code>PaymentResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `payment_reference` | string | yes |  |
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `subscription_id` | integer (nullable) | yes |  |
| `amount` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `payment_provider` | PaymentProvider | yes |  |
| `payment_method` | string (nullable) | yes |  |
| `gateway_transaction_id` | string (nullable) | yes |  |
| `status` | PaymentStatus | yes |  |
| `payment_date` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### Payment statistics

`GET /payments/summary`

**Requires** `Authorization: Bearer <token>`.

Aggregate payment counts by status (pending, successful, failed, cancelled, refunded, expired) plus total revenue.

**Responses**

- `200 OK` Returns `PaymentStatsResponse`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `403 Forbidden` -- Admin account is inactive.

<details><summary><code>PaymentStatsResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `total_payments` | integer | yes |  |
| `pending_payments` | integer | yes |  |
| `successful_payments` | integer | yes |  |
| `failed_payments` | integer | yes |  |
| `cancelled_payments` | integer | yes |  |
| `refunded_payments` | integer | yes |  |
| `expired_payments` | integer | yes |  |
| `total_revenue` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |

</details>


### Get a payment

`GET /payments/{payment_reference}`

**Requires** `Authorization: Bearer <token>`.

Returns a single payment by its reference.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `payment_reference` | path | string | yes | -- |

**Responses**

- `200 OK` Returns `PaymentResponse`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `404 Not Found` -- Payment not found.

<details><summary><code>PaymentResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `payment_reference` | string | yes |  |
| `customer_id` | integer | yes |  |
| `plan_id` | integer | yes |  |
| `subscription_id` | integer (nullable) | yes |  |
| `amount` | string | yes | pattern: ^(?!^[-+.]*$)[+-]?0*\d*\.?\d*$ |
| `payment_provider` | PaymentProvider | yes |  |
| `payment_method` | string (nullable) | yes |  |
| `gateway_transaction_id` | string (nullable) | yes |  |
| `status` | PaymentStatus | yes |  |
| `payment_date` | string<date-time> (nullable) | yes |  |
| `created_at` | string<date-time> | yes |  |
| `updated_at` | string<date-time> | yes |  |

</details>


### List a customer's payments

`GET /payments/customer/{customer_id}`

**Requires** `Authorization: Bearer <token>`.

Returns every payment made by a customer.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `customer_id` | path | integer | yes | -- |

**Responses**

- `200 OK` Returns `PaymentResponse (array)`.
- `422 Validation Error` -- Validation Error Returns `HTTPValidationError`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.



---

## Automation

Manually triggered background maintenance jobs (payments, subscriptions, routers, notifications).

### Run all automation jobs

`POST /automation/all`

**Requires** `Authorization: Bearer <token>`.

Runs every background maintenance job (payments, subscriptions, routers, notifications) in one call and logs a single audit entry. Rate limited to 10 requests/minute.

**Responses**

- `200 OK`
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `429 Too Many Requests` -- Too many requests -- rate limit exceeded.


### Run payment maintenance

`POST /automation/payments`

**Requires** `Authorization: Bearer <token>`.

Runs payment reconciliation/expiry maintenance. Rate limited to 10 requests/minute.

**Responses**

- `200 OK` Returns `JobResultResponse`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `429 Too Many Requests` -- Too many requests -- rate limit exceeded.

<details><summary><code>JobResultResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `processed` | integer | yes |  |
| `message` | string | yes |  |

</details>


### Run subscription maintenance

`POST /automation/subscriptions`

**Requires** `Authorization: Bearer <token>`.

Expires due subscriptions and activates queued ones whose turn has come. Rate limited to 10 requests/minute.

**Responses**

- `200 OK` Returns `JobResultResponse`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `429 Too Many Requests` -- Too many requests -- rate limit exceeded.

<details><summary><code>JobResultResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `processed` | integer | yes |  |
| `message` | string | yes |  |

</details>


### Run router maintenance

`POST /automation/routers`

**Requires** `Authorization: Bearer <token>`.

Runs router account provisioning/sync/retry maintenance. Rate limited to 10 requests/minute.

**Responses**

- `200 OK` Returns `JobResultResponse`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `429 Too Many Requests` -- Too many requests -- rate limit exceeded.

<details><summary><code>JobResultResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `processed` | integer | yes |  |
| `message` | string | yes |  |

</details>


### Run notification scheduling

`POST /automation/notifications`

**Requires** `Authorization: Bearer <token>`.

Runs due notification scheduling (reminders, expiry notices, etc.). Rate limited to 10 requests/minute.

**Responses**

- `200 OK` Returns `JobResultResponse`.
- `401 Unauthorized` -- Missing, invalid, or expired bearer token.
- `429 Too Many Requests` -- Too many requests -- rate limit exceeded.

<details><summary><code>JobResultResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `processed` | integer | yes |  |
| `message` | string | yes |  |

</details>



---

## Session

Telegram bot conversational session/state resolution.

### Resolve Telegram session state

`GET /session/telegram/{telegram_user_id}`

No authentication required.

Given a Telegram user ID, returns what the bot should do next: the next onboarding step, a message to show, a keyboard layout, and the customer record if one exists. This is the core state-machine endpoint the Telegram bot polls to decide what screen to show. `first_login` marks a brand-new chat. Not authenticated. Rate limited to 30 requests/minute.

**Parameters**

| Name | In | Type | Required | Default |
|---|---|---|---|---|
| `telegram_user_id` | path | integer | yes | -- |
| `first_login` | query | boolean | no | False |

**Responses**

- `200 OK` Returns `SessionResponse`.
- `422 Validation Error` -- Request body or query parameters failed validation.
- `429 Too Many Requests` -- Too many requests -- rate limit exceeded.

<details><summary><code>SessionResponse</code> fields</summary>

| Field | Type | Required | Notes |
|---|---|---|---|
| `next_action` | NextAction | yes |  |
| `message` | string | yes |  |
| `keyboard` | string | yes |  |
| `customer` | CustomerResponse (nullable) | no |  |

</details>



---

## Health

Service liveness check.

### Health check

`GET /health/`

No authentication required.

Basic liveness probe. Returns service status and a timestamp. Not authenticated.

**Responses**

- `200 OK`

