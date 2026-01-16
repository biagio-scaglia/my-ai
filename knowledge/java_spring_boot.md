# Java & Spring Boot Essentials

## Java Moderno (17+)

- **Records**: Classi immutabili concise (`public record User(String name) {}`).
- **Var**: Inferenza tipi locale (`var list = new ArrayList<String>();`).
- **Streams API**: Manipolazione funzionale collezioni.

## Spring Boot

Standard de-facto per microservizi Java.

### Annotation Cheatsheet

- `@SpringBootApplication`: Punto di ingresso.
- `@RestController`: Definisce API JSON.
- `@Service`: Logica di business.
- `@Repository`: Accesso dati (JPA).
- `@Autowired`: Dependency Injection automatica.

### Esempio Controller

```java
@RestController
@RequestMapping("/api/v1/users")
public class UserController {

    private final UserService service;

    public UserController(UserService service) {
        this.service = service;
    }

    @GetMapping
    public List<User> getAll() {
        return service.findAll();
    }
}
```
