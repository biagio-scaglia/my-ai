# Ruby & Ruby on Rails Mastery

## Ruby Basics

- **Paradigma**: Orientato agli oggetti puro (tutto è un oggetto).
- **Sintassi**: Pulita, simile all'inglese.
- **Blocchi**: `do ... end` o `{ ... }`.

### Esempio Loop

```ruby
# Times loop
5.times do |i|
  puts "Giro numero #{i}"
end

# Each loop (su array)
users.each do |user|
  puts user.name
end
```

## Ruby on Rails (RoR)

Framework MVC (Model-View-Controller) "Opinionated".

- **Concept**: Convention over Configuration.
- **ActiveRecord**: ORM potente.

### Struttura

- `app/models`: Logica dati.
- `app/controllers`: Logica di business e routing.
- `app/views`: Template HTML (ERB).

### Comandi Utili

- `rails new projectname`: Crea progetto.
- `rails g scaffold User name:string email:string`: Crea CRUD completo.
- `rails db:migrate`: Applica modifiche al DB.
