export interface DatabaseConnectionRequest {
  db_type: "postgresql" | "mysql" | "sqlite";
  host: string;
  port: number;
  username: string;
  password: string;
  database: string;
}

export interface DatabaseConnectionResponse {
  success: boolean;
  message: string;
  database_type: string;
  schema: Record<string, any> | null;
}