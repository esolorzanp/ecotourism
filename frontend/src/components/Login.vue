<template>
    <main class="container">
        <form class="form">
            <h1 class="form__title">Login</h1>
            <div class="form-floating mb-3">
                <input type="email" class="form-control" id="floatingInput" placeholder="name@example.com">
                <label for="floatingInput">Corre electrónico</label>
            </div>
            <div class="form-floating mb-3">
                <input type="password" class="form-control" id="floatingInput" placeholder="name@example.com">
                <label for="floatingInput">Contraseña</label>
            </div>
            <div class="form__buttonsgroup">
                <button type="submit" class="form__button btn btn-primary">Ingresar</button>
                <button type="submit" class="form__button btn btn-secondary">Limpiar</button>
            </div>
        </form>
    </main>
</template>
<script setup>
</script>
<style scoped>
.form{
    width: 700px;
    margin: 0 auto;
    margin-top: 150px;
}
</style>