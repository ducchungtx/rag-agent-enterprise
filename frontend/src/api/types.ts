export type MemberRole = "owner" | "admin" | "contributor" | "viewer";

export interface UserOut {
  id: string;
  email: string;
  username: string;
}

export interface TokenOut {
  access_token: string;
  token_type: string;
}

export interface TenantOut {
  id: string;
  name: string;
  created_at: string;
}

export interface KBOut {
  id: string;
  tenant_id: string;
  owner_user_id: string;
  name: string;
  description: string;
  created_at: string;
}

export interface DocumentOut {
  id: string;
  kb_id: string;
  tenant_id: string;
  title: string;
  parse_status: "pending" | "processing" | "completed" | "failed";
  error_message: string | null;
  created_at: string;
}

export interface CitationOut {
  chunk_id: string;
  document_id: string;
  title: string;
  content: string;
  score: number;
}

export interface ChatOut {
  answer: string;
  citations: CitationOut[];
  refused?: boolean;
  refusal_reason?: string | null;
  suggested_message?: string | null;
}

export interface MemberOut {
  user_id: string;
  email: string;
  username: string;
  role: MemberRole;
  status: string;
}

export interface APIKeyOut {
  id: string;
  name: string;
  key_prefix: string;
  capabilities: string[];
  kb_allowlist: string[] | null;
  created_at: string;
  raw_key?: string | null;
}
