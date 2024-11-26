<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const perfiles = ref([])
const errorMessage = ref('')
const successMessage = ref('')

// Variables de captura
const inDescripcion = ref('')
const inDetalle = ref('')
const inUrl = ref('')

// Función para obtener el perfil y verificar permisos
const checkPermissions = () => {
    const token = localStorage.getItem('token')

    if (token) {
        const decodedToken = jwtDecode(token)
        const perfil = decodedToken.sub.perfil_id

        if (perfil !== 2) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
            router.push('/menu')
            return false
        }
        return token  // Retornamos el token si es empleado o supervisor
    } else {
        router.push('/login')
        return false
    }
}

// Función para crear sitio
const createSitio = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.post(
            'http://127.0.0.1:5000/sitios',
            {
                "descripcion": inDescripcion.value,
                "detalle": inDetalle.value,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
        if (response.status === 201) {
            successMessage.value = 'Sitio creado exitosamente.'
            errorMessage.value = ''
            limpiar()
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al crear el sitio'
        successMessage.value = ''
    }
}

const limpiar = () => {
    inDescripcion.value = ''
    inDetalle.value = ''
}

// Volver al menú principal
const goBack = () => {
    router.push('/sitios-list')
}

// Verificar permisos al montar el componente
onMounted(() => {
    checkPermissions()
})
</script>

<template>
    <main class="container">
        <form class="form" @submit.prevent="createSitio">
            <h1 class="form__title">Creación de Sitios</h1>
            <section>
                <p v-if="errorMessage" class="alert alert-danger">{{ errorMessage }}</p>
                <p v-if="successMessage" class="alert alert-success">{{ successMessage }}</p>
                <div class="form-floating mb-3">
                    <input v-model="inDescripcion" type="text" class="form-control" id="floatingDescripcion"
                        placeholder="Ingrese la descripcion" :required="true">
                    <label for="floatingDescripcion">Descripcion</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inDetalle" type="text" class="form-control" id="floatingDetalle"
                        placeholder="Ingrese la descripción" :required="true">
                    <label for="floatingDetalle">Detalle</label>
                </div>

                <!-- Buttons group-->
                <div class="form__buttonsgroup">
                    <button type="submit" class="form__button btn btn-primary">Agregar</button>
                    <button @click="limpiar" class="form__button btn btn-secondary">Limpiar</button>
                    <button @click="goBack" class="form__button btn btn-secondary">Regresar al menú</button>
                </div>
            </section>
        </form>
    </main>

</template>

<style scoped></style>