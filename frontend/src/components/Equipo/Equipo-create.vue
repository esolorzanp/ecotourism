<script setup>
import { ref, onMounted } from 'vue'
import { useRouter } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const errorMessage = ref('')
const successMessage = ref('')

// Variables de captura
const inNombre = ref('')
const inCargo = ref('')
const inEdad = ref('')
const inGenero = ref('')
const inHobbies = ref('')
const inConocimientos = ref('')

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

// Función para crear integrante de equipo
const createEquipo = async () => {
    const token = checkPermissions()
    if (!token) return
    if (!camposValidos()) return

    try {
        const response = await axios.post(
            'http://127.0.0.1:5000/equipo',
            {
                "nombre": inNombre.value,
                "cargo": inCargo.value,
                "edad": inEdad.value,
                "genero": inGenero.value,
                "hobbies": inHobbies.value,
                "conocimientos": inConocimientos.value
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
        if (response.status === 201) {
            successMessage.value = 'Integrante de equipo creado exitosamente.'
            errorMessage.value = ''
            limpiar()
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al crear el integrante del equipo'
        successMessage.value = ''
    }
}

const camposValidos = () => {
    /*
    if (inClave.value != inClaveConfirmada.value) {
        errorMessage.value = 'La constraseña y su confirmación no son las mismas'
        successMessage.value = ''
        return false
    }*/
    return true
}

const limpiar = () => {
    inNombre.value = ''
    inCargo.value = ''
    inEdad.value = ''
    inGenero.value = ''
    inHobbies.value = ''
    inConocimientos.value = ''
}

// Volver al menú principal
const goBack = () => {
    router.push('/equipo-list')
}

// Verificar permisos al montar el componente
onMounted(() => {
    checkPermissions()
})
</script>

<template>

    <main class="container">
        <form class="form" @submit.prevent="createEquipo">
            <h1 class="form__title">Creación de integrantes de equipo</h1>
            <section>
                <p v-show="errorMessage" class="alert alert-danger">{{ errorMessage }}</p>
                <p v-show="successMessage" class="alert alert-success">{{ successMessage }}</p>
                <div class="form-floating mb-3">
                    <input v-model="inNombre" type="text" class="form-control" id="floatingNombre"
                        placeholder="Ingrese el nombre" :required="true">
                    <label for="floatingNombre">Nombres</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inCargo" type="text" class="form-control" id="floatingCargo"
                        placeholder="Ingrese el cargo" :required="true">
                    <label for="floatingCargo">Cargo</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inEdad" type="text" class="form-control" id="floatingEdad"
                        placeholder="Ingrese la edad" :required="true">
                    <label for="floatingEdad">Edad</label>
                </div>
                <div class="form-floating">
                    <select v-model="inGenero" class="form-select" id="floatingSelect" aria-label="Floating label select example">
                        <option selected>Selecione el género</option>
                    <option value="Masculino">Masculino</option>
                    <option value="Femenino">Femenino</option>
                    </select>
                    <label for="floatingSelect">Selecione el género</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inHobbies" type="text" class="form-control" id="floatingHobbies"
                        placeholder="Ingrese los hobbies" :required="true">
                    <label for="floatingHobbies">Hobbies</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inConocimientos" type="text" class="form-control" id="floatingConocimientos"
                        placeholder="Ingrese los conocimientos" :required="true">
                    <label for="floatingConocimientos">Conocimientos</label>
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