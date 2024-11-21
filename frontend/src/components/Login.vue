<template>
    <main class="container">
        <form>
            <h1 class="title">Login</h1>
            <div class="form-floating mb-3">
                <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
                <label for="floatingInput">Corre electrónico</label>
            </div>
            <div class="form-floating mb-3">
                <input type="password" class="form-control" id="floatingInput" placeholder="name@example.com">
                <label for="floatingInput">Contraseña</label>
            </div>
            <button type="submit" class="btn btn-primary">Ingresar</button>
            <button type="submit" class="btn btn-success">Limpiar</button>
        </form>
    </main>
</template>
<script setup>
</script>
<style scoped>
form {
    max-width: 500px;
    padding: 2rem;
    border: 1px solid lightgray;
    border-radius: 12px;
    margin: 100px auto;
    display: flex;
    flex-direction: column;
}

form h1 {
    text-align: center;
    padding-bottom: 3rem;
    font-size: 48px;
}
</style>