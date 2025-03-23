const HOST = 'http://127.0.0.1:8249'

export type Dict = Record<string, any>

interface ExtReqInit extends RequestInit {
  params?: { [index: string]: string }
  json?: any
}

/**
 * Modify a fetch url
 *
 * @param input Fetch url input
 * @param callback Callback for modification
 */
export function reconstructUrl(input: URL | RequestInfo, callback: (url: URL) => URL | void): RequestInfo | URL {
  let u = new URL((input instanceof Request) ? input.url : input)
  const result = callback(u)
  if (result) u = result
  if (input instanceof Request) {
    // @ts-ignore
    return { url: u, ...input }
  }
  return u
}

/**
 * Fetch with url parameters
 */
export function fetchWithParams(input: URL | RequestInfo, init?: ExtReqInit): Promise<Response> {
  return fetch(reconstructUrl(input, u => {
    u.search = new URLSearchParams(init?.params ?? {}).toString()
  }), init)
}

/**
 * Do something with the response when it's not ok
 *
 * @param res Response object
 */
async function ensureOk(res: Response) {
  if (!res.ok) {
    const text = await res.text()
    console.error(`${res.status}: ${text}`)

    // If 400 invalid token is caught, should invalidate the token and redirect to signin
    if (text === 'Invalid token') {
      localStorage.removeItem('token')
      window.location.href = '/'
    }

    // Try to parse as json
    let json
    try {
      json = JSON.parse(text)
    } catch (e) {
      throw new Error(text)
    }
    if (json.error) throw new Error(json.error)
  }
}

/**
 * Post to an endpoint and return the response in JSON while doing error checks
 * and handling token (and token expiry) automatically.
 *
 * @param endpoint The endpoint to post to (e.g., '/pull')
 * @param params An object containing the request body or any necessary parameters
 * @param init Additional fetch/init configuration
 * @returns The JSON response from the server
 */
export async function post(endpoint: string, params: Dict = {}, init?: ExtReqInit): Promise<any> {
  return postHelper(endpoint, params, init).then(it => it.json())
}

/**
 * Actual impl of post(). This does not return JSON but returns response object.
 */
async function postHelper(endpoint: string, params: Dict = {}, init?: ExtReqInit): Promise<any> {
  // Add token if exists
  const token = localStorage.getItem('token')
  if (token && !('token' in params)) params = { ...(params ?? {}), token }

  if (init?.json) {
    init.body = JSON.stringify(init.json)
    init.headers = { 'Content-Type': 'application/json', ...init.headers }
    init.json = undefined
  }

  const res = await fetchWithParams(HOST + endpoint, { method: 'POST', params, ...init })
    .catch(e => { console.error(e); throw new Error("Network error") })
  await ensureOk(res)

  return res
}