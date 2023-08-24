"""
Define a defualt implementation of functions
to be used to call chat-completion API.
refer to : https://github.com/openai/openai-cookbook/blob/main/examples/How_to_call_functions_with_chat_models.ipynb
"""
test_schema = """
Table : Album
Columns: AlbumId,Title,ArtistId
Table : Artist
Columns: ArtistId,Name
Table : Customer
Columns: CustomerId,FirstName,LastName,Company,Address,City,State,Country,PostalCode,Phone,Fax,Email,SupportRepId
Table : Employee
Columns: EmployeeId,LastName,FirstName,Title,ReportsTo,BirthDate,HireDate,Address,City,State,Country,PostalCode,Phone,Fax,Email
Table : Genre
Columns: GenreId,Name
Table : Invoice
Columns: InvoiceId,CustomerId,InvoiceDate,BillingAddress,BillingCity,BillingState,BillingCountry,BillingPostalCode,Total
Table : InvoiceLine
Columns: InvoiceLineId,InvoiceId,TrackId,UnitPrice,Quantity
Table : MediaType
Columns: MediaTypeId,Name
Table : Playlist
Columns: PlaylistId,Name
Table : PlaylistTrack
Columns: PlaylistId,TrackId
Table : Track
Columns: TrackId,Name,AlbumId,MediaTypeId,GenreId,Composer,Milliseconds,Bytes,UnitPrice"""


test_query_gen_messages = []

test_query_gen_messages.append(
    {
        "role": "system",
        "content": "Anwer User's questions by generating SQL queries against database schema provided in functions",
    }
)
test_query_gen_messages.append(
    {"role": "user", "content": "Hi, who are the top 5 artists by number of tracks?"}
)


incorrect_sql = """SELECT Artist.Name, COUNT() AS NumTracks FROM Artist JOIN Album ON Artist.ArtistId = Album.ArtistId JOIN Track ON Album.AlbumId = Track.AlbumId GROUP BY Artist.Name ORDER BY NumTracks DESC LIMIT 5;"""

error_message = "Syntax Error near COUNT"
test_correction_messages = []
test_correction_messages.append(
    {
        "role": "system",
        "content": "Correct the the SQL query given by user using error_message and supplement_info",
    },
)

test_correction_messages.append(
    {
        "role": "user",
        "content": f"""Incorrect SQL Query is delimited by `` : ``{incorrect_sql}`` and error_message : {error_message}""",
    },
)


test_basic_messages = [{"role": "user", "content": "Pagani"}]

FUNCTION_ARRAY = [
    {
        "name": "query_database",
        "description": """Answer user's question against a database.Argument should be a fully formed SQL query""",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": """SQL query extracting data to answer user's question.
                    SQL should be written using following schema delimited by ```:
                    ```$schema```.\nThe query should be returned in plain text,not in JSON.""",
                }
            },
            "required": ["query"],
        },
    },
    {
        "name": "rectify_sql",
        "description": "correct the SQL 'query' based on 'error_message' and 'supplement_info' provided by user",
        "parameters": {
            "type": "object",
            "properties": {
                "query": {
                    "type": "string",
                    "description": "Corrected SQL query based on error_message and supplement_info",
                },
                "error_message": {
                    "type": "string",
                    "description": "the error message providing details to correct he SQL query",
                },
                "supplement_info": {
                    "type": "string",
                    "description": "Additional Information provided by user to help in correcting query. This is an optional argument",
                },
            },
            "required": ["query", "error_message"],
        },
    },
]
