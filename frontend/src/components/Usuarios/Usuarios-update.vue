<script setup>
import { ref, onMounted } from 'vue'
import { useRouter, useRoute } from 'vue-router'
import { jwtDecode } from 'jwt-decode'
import axios from 'axios'

const router = useRouter()
const route = useRoute()
const perfiles = ref([])
const errorMessage = ref('')
const successMessage = ref('')

// Variables de captura
const inId = route.params.id
const inNombre = ref('')
const inCorreo = ref('')
const inClave = ref('')
const inPerfil = ref('')
const inClaveConfirmada = ref('')


// Función para obtener el perfil y verificar permisos
const checkPermissions = () => {
    const token = localStorage.getItem('token')

    if (token) {
        const decodedToken = jwtDecode(token)
        const perfil = decodedToken.sub.perfil_id

        if (perfil !== 1) {
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

// Función para cargar perfiles si se tienen permisos
const fetchPerfiles = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get('http://127.0.0.1:5000/usuariosperfiles', {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            perfiles.value = response.data
        }

    } catch (error) {
        if (error.response && error.response.status === 403) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
            successMessage.value = ''
        } else {
            errorMessage.value = 'Error al cargar los perfiles.'
            successMessage.value = ''
        }
        successMessage.value = ''
    }
}


// Función para cargar un usuario si se tienen permisos
const fetchUsuario = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get(`http://127.0.0.1:5000/usuarios/${inId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            const usuario = response.data
            inNombre.value = usuario.nombre
            inCorreo.value = usuario.correo
            inPerfil.value = usuario.id_perfil
            successMessage.value = ''
            errorMessage.value = ''
        }

    } catch (error) {
        if (error.response && error.response.status === 403) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
        } else {
            errorMessage.value = 'Error al cargar los usuarios.'
        }
    }
}

// Función para crear usuario
const updateUser = async () => {
    const token = checkPermissions()
    if (!token) return
    if (!camposValidos()) return

    try {
        const response = await axios.put(
            `http://127.0.0.1:5000/usuarios/${inId}`,
            {
                "nombre": inNombre.value,
                "correo": inCorreo.value,
                "clave": inClave.value,
                "perfil": inPerfil.value
            },
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
        if (response.status === 201) {
            successMessage.value = 'Usuario modificado exitosamente.'
            errorMessage.value = ''
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al crear el usuario. (catch)'
        successMessage.value = ''
    }
}

const camposValidos = () => {
    if (inClave.value != inClaveConfirmada.value) {
        errorMessage.value = 'La constraseña y su confirmación no son las mismas'
        successMessage.value = ''
        return false
    }
    return true
}

const limpiar = () => {
    inNombre.value = ''
    inCorreo.value = ''
    inClave.value = ''
    inPerfil.value = ''
    inClaveConfirmada.value = ''
}

// Volver al menú principal
const goBack = () => {
    router.push('/usuarios-list')
}

// Verificar permisos al montar el componente
// Cargar perfiles al montar el componente
onMounted(() => {
    //checkPermissions()
    fetchPerfiles()
    fetchUsuario()
})
</script>

<template>
    <main class="container">
        <form class="form" @submit.prevent="updateUser">
            <h1 class="form__title">Actualización de usuario</h1>
            <section>
                <p v-show="errorMessage" class="alert alert-danger">{{ errorMessage }}</p>
                <p v-show="successMessage" class="alert alert-success">{{ successMessage }}</p>
                <div class="form-floating mb-3">
                    <input v-model="inNombre" type="text" class="form-control" id="floatingNombre"
                        placeholder="Ingrese el nombre" :required="true">
                    <label for="floatingNombre">Nombres</label>
                </div>
                <div class="form-floating mb-3">
                    <input v-model="inCorreo" type="text" class="form-control" id="floatingCorreo"
                        placeholder="name@example.com" :required="true">
                    <label for="floatingCorreo">Correo</label>
                </div>
                <select v-model="inPerfil" v-if="perfiles.length > 0" class="form-select"
                    aria-label="Default select example" :required="true">
                    <option value="" selected>Seleccione un perfil</option>
                    <option v-for="perfil in perfiles" :key="perfil.id" :value="perfil.id">{{
                        perfil.descripcion }}</option>
                </select>

                <!-- Buttons group-->
                <div class="form__buttonsgroup">
                    <button type="submit" class="form__button btn btn-primary">Actualizar</button>
                    <button @click="limpiar" class="form__button btn btn-secondary">Limpiar</button>
                    <button @click="goBack" class="form__button btn btn-secondary">Regresar a la lista</button>
                </div>
            </section>
        </form>
    </main>
</template>

<style scoped></style>