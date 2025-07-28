# Books and Movies library

A CRUD API to create, read, update and delete your movies and books of your library.

## API Endpoints

Main API endpoints.

### Auth

- `POST /api/register` - Register new user
- `POST /api/login` - Login user

### Books

- `GET /api/books` - Get all books
- `POST /api/books/create` - Create a new book
- `POST /api/books/detail/{id}` - Get a book by ID
- `POST /api/books/update/{id}` - Update book
- `POST /api/books/delete/{id}` - Delete book

### Movies

- `GET /api/movies` - Get all movies
- `POST /api/movies/create` - Create a new movie
- `POST /api/movies/detail/{id}` - Get a movie by ID
- `POST /api/movies/update/{id}` - Update movie
- `POST /api/movies/delete/{id}` - Delete movie
