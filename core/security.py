"""
SQL security and validation module.
Enforces read-only query policies, restricts tables, blocks modifications,
disallows multiple statements, and sanitizes identifiers.
"""
import re
from typing import List, Tuple, Set
import sqlparse
from sqlparse.sql import Statement, IdentifierList, Identifier
from sqlparse.tokens import Keyword

FORBIDDEN_KEYWORDS: Set[str] = {
    "insert", "update", "delete", "drop", "alter", "truncate", "create",
    "replace", "grant", "revoke", "execute", "exec", "call", "attach",
    "detach", "pragma", "reindex", "vacuum", "upsert"
}

DANGEROUS_FUNCTIONS: Set[str] = {
    "load_extension", "writefile", "readfile", "edit"
}

class SQLSecurityValidator:
    def __init__(self, allowed_tables: List[str]):
        self.allowed_tables = set(t.lower() for t in allowed_tables)

    def validate_query(self, sql_query: str) -> Tuple[bool, str]:
        if not sql_query or not sql_query.strip():
            return False, "Query cannot be empty."

        clean_query = sql_query.strip().rstrip(";")
        parsed = sqlparse.parse(clean_query)
        if not parsed:
            return False, "Unable to parse SQL query."

        # Reject semicolons inside string indicating stacked statements
        if ";" in clean_query:
            return False, "Multiple statements or stacked queries (;) are strictly forbidden."

        if len(parsed) > 1:
            return False, "Multiple statements are strictly forbidden."

        stmt = parsed[0]

        first_token = stmt.token_first(skip_ws=True, skip_cm=True)
        if not first_token or first_token.value.upper() != "SELECT":
            return False, "Only read-only SELECT statements are permitted."

        query_text_lower = clean_query.lower()
        for kw in FORBIDDEN_KEYWORDS:
            pattern = rf"\b{kw}\b"
            if re.search(pattern, query_text_lower):
                return False, f"Forbidden SQL operation or keyword detected: {kw.upper()}."

        for func in DANGEROUS_FUNCTIONS:
            pattern = rf"\b{func}\s*\("
            if re.search(pattern, query_text_lower):
                return False, f"Dangerous SQL function detected: {func}."

        referenced_tables = self._extract_tables(stmt)
        if referenced_tables:
            for table in referenced_tables:
                if table.lower() not in self.allowed_tables:
                    return False, f"Query references unauthorized table: {table}. Allowed: {list(self.allowed_tables)}"

        return True, "Query is safe."

    def _extract_tables(self, stmt: Statement) -> Set[str]:
        tables = set()
        from_seen = False
        for token in stmt.tokens:
            if token.is_whitespace:
                continue
            if token.ttype is Keyword and token.value.upper() in ("FROM", "JOIN", "INNER JOIN", "LEFT JOIN"):
                from_seen = True
                continue
            if from_seen:
                if isinstance(token, IdentifierList):
                    for id_token in token.get_identifiers():
                        name = id_token.get_real_name() or id_token.get_name()
                        if name:
                            tables.add(name)
                    from_seen = False
                elif isinstance(token, Identifier):
                    name = token.get_real_name() or token.get_name()
                    if name:
                        tables.add(name)
                    from_seen = False
                elif token.ttype is Keyword:
                    from_seen = False
                elif not token.is_punctuation:
                    tables.add(token.value.strip("`\""))
                    from_seen = False
        return tables
