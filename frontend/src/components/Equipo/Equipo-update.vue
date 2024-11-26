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


// Función para cargar un usuario si se tienen permisos
const fetchEquip = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get(`http://127.0.0.1:5000/equipo/${inId}`, {
            headers: {
                Authorization: `Bearer ${token}`,
            },
        })

        if (response.status === 201) {
            const equip = response.data
            inNombre.value = equip.nombre
            inCargo.value = equip.cargo
            inEdad.value = equip.edad
            inGenero.value = equip.genero
            inHobbies.value = equip.hobbies
            inConocimientos.value = equip.conocimientos
            successMessage.value = ''
            errorMessage.value = ''
        }

    } catch (error) {
        if (error.response && error.response.status === 403) {
            errorMessage.value = 'No tienes permiso para ver esta página.'
        } else {
            errorMessage.value = 'Error al cargar los integrantes de equipo.'
        }
    }
}

// Función para actualizar integrante de equipo
const updateEquipo = async () => {
    const token = checkPermissions()
    if (!token) return
    if (!camposValidos()) return
    if (!readEquipoNombre()) return

    try {
        const response = await axios.put(
            `http://127.0.0.1:5000/equipo/${inId}`,
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
            successMessage.value = 'Integrante de equipo actualizado exitosamente.'
            errorMessage.value = ''
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al actualizar el integrante del equipo'
        successMessage.value = ''
    }
}

// Función para validar integrate de equipo que no exista otro por nombre
const readEquipoNombre = async () => {
    const token = checkPermissions()
    if (!token) return

    try {
        const response = await axios.get(
            `http://127.0.0.1:5000/equipo/${inNombre.value}`,
            //{},
            {
                headers: {
                    Authorization: `Bearer ${token}`,
                },
            }
        )
        if (response.status === 201 && response.data.length > 0) {
            successMessage.value = ''
            errorMessage.value = 'Integrante de equipo ya existe con este nombre'
            return false
        } else {
            successMessage.value = ''
            errorMessage.value = ''
            return true
        }
    } catch (error) {
        errorMessage.value = error.response?.data?.message || 'Error al leer el integrante de equipo por nombre'
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
    //checkPermissions()
    fetchEquip()
})
</script>

<template>
    <main class="container">
        <form class="form" @submit.prevent="updateEquipo">
            <h1 class="form__title">Actualización de integrantes de equipo</h1>
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
                    <button type="submit" class="form__button btn btn-primary">Actualizar</button>
                    <button @click="limpiar" class="form__button btn btn-secondary">Limpiar</button>
                    <button @click="goBack" class="form__button btn btn-secondary">Regresar a la lista</button>
                </div>
            </section>
        </form>
    </main>
</template>

<style scoped></style>