<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const errorMessage = ref('')
const successMessage = ref('')

// Variables de captura
const inId = route.params.id
const inPregunta = ref('')
const inRespuesta = ref('')
const inOrden = ref('')

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
        return token  // Retornamos el token si es administrador
    } else {
        router.push('/login')
        return false
    }
}

// Función para cargar una pregunta frecuente si se tienen permisos
const fetchPreguntasFrecuentes = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get(`http://127.0.0.1:5000/preguntasfrecuentes/${inId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            const pf = response.data
            inPregunta.value = pf.pregunta
            inRespuesta.value = pf.respuesta
            inOrden.value = pf.orden
            successMessage.value = ''
            errorMessage.value = ''
        }

    } catch (error) {
        if (error.response && error.response.status === 403) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
        } else {
            errorMessage.value = 'Error al cargar preguntas frecuentes.'
        }
    }
}

// Función para crear Preguntas frecuentes
const updatePreguntasFrecuentes = async () => {
    const token = checkPermissions()
    if (!token) return
    if (!camposValidos()) return

    try {
        const response = await axios.put(
            `http://127.0.0.1:5000/preguntasfrecuentes/${inId}`,
            {
                "pregunta": inPregunta.value,
                "respuesta": inRespuesta.value,
                "orden": inOrden.value,
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
        if (response.status === 201) {
            successMessage.value = 'Pregunta frecuente modificada exitosamente.'
            errorMessage.value = ''
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al actualizar las preguntas frecuentes'
        successMessage.value = ''
    }
}

const camposValidos = () => {
    /*if (inClave.value != inClaveConfirmada.value) {
        errorMessage.value = 'La constraseña y su confirmación no son las mismas'
        successMessage.value = ''
        return false
    }*/
    return true
}

const limpiar = () => {
    inPregunta.value = ''
    inRespuesta.value = ''
    inOrden.value = ''
}

// Volver al menú principal
const goBack = () => {
    router.push('/preguntasfrecuentes-list')
}

// Verificar permisos al montar el componente
// Cargar perfiles al montar el componente
onMounted(() => {
    fetchPreguntasFrecuentes()
})

</script>

<template>
    <main class="container">
        <form class="form" @submit.prevent="updatePreguntasFrecuentes">
            <h1 class="form__title">Actualización de preguntas frecuentes</h1>
            <section>
                <p v-show="errorMessage" class="alert alert-danger">{{ errorMessage }}</p>
                <p v-show="successMessage" class="alert alert-success">{{ successMessage }}</p>
                <div class="form-floating mb-3">
                    <input v-model="inPregunta" type="text" class="form-control" id="floatingPregunta"
                        placeholder="Ingrese el texto de la pregunta" :required="true">
                    <label for="floatingPregunta">Pregunta</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inRespuesta" type="text" class="form-control" id="floatingRespuesta"
                        placeholder="Ingrese el texto de la respuesta" :required="true">
                    <label for="floatingRespuesta">Respuesta</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inOrden" type="text" class="form-control" id="floatingOrden"
                        placeholder="Ingrese el orden de la pregunta" :required="true">
                    <label for="floatingOrden">Orden</label>
                </div>

                <!-- Buttons group-->
                <div class="form__buttonsgroup">
                    <button type="submit" class="form__button btn btn-primary">Actualizar</button>
                    <button @click="limpiar" class="form__button btn btn-secondary">Limpiar</button>
                    <button @click="goBack" class="form__button btn btn-secondary">Regresar al menú</button>
                </div>
            </section>
        </form>
    </main>
</template>
<style scoped></style>