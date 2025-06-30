<template>
  <div class="min-h-screen flex items-center justify-center px-2 py-8" :style="{ background: 'var(--theme-bg)' }">
    <Card variant="interactive" className="w-full max-w-md mx-auto flex flex-col items-center relative animate-profile-fadein">
      <!-- Logo Dividis -->
      <svg style="width:56px;height:56px;margin-bottom:1.5rem;" viewBox="0 0 56 56" fill="none" xmlns="http://www.w3.org/2000/svg">
        <circle cx="28" cy="28" r="28" :fill="`var(--theme-accent, #fff)`" fill-opacity="0.08"/>
        <path d="M20 16h8a8 8 0 1 1 0 24h-8V16z" :fill="`var(--theme-accent, #fff)`" fill-opacity="0.95"/>
        <rect x="24" y="22" width="12" height="2.5" rx="1.25" :fill="`var(--theme-border, #3b82f6)`"/>
      </svg>
      <div class="text-center mb-6">
        <h1 class="text-2xl font-bold mb-2" :style="{
          background: 'linear-gradient(90deg, var(--theme-accent), var(--theme-border))',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent'
        }">Perfil de Usuario</h1>
      </div>
      <form class="w-full flex flex-col gap-4" @submit.prevent="handleSubmit">
        <input
          class="input-theme"
          v-model="firstName"
          placeholder="Nombre"
          type="text"
        />
        <input
          class="input-theme"
          v-model="lastName"
          placeholder="Apellido"
          type="text"
        />
        <input
          class="input-theme"
          v-model="email"
          placeholder="Correo electrónico"
          type="email"
          autocomplete="email"
        />
        <select
          class="input-theme"
          v-model="selectedTheme"
          @change="onThemeChange"
        >
          <option v-for="theme in themes" :key="theme.key" :value="theme.key">
            {{ theme.label }}
          </option>
        </select>
        <button :disabled="loading" type="submit" class="btn-theme w-full mt-4">
          {{ loading ? 'Guardando...' : 'Guardar' }}
        </button>
        <transition name="fade">
          <p v-if="success" class="mt-2 text-center" :style="{ color: 'var(--theme-accent)' }">{{ success }}</p>
        </transition>
        <p v-if="error" class="mt-2 text-center" :style="{ color: 'var(--theme-border)' }">{{ error }}</p>
      </form>
      <router-link
        to="/dashboard"
        class="mt-6 block text-center"
        :style="{ color: 'var(--theme-border)' }"
        aria-label="Volver al dashboard"
      >
        <svg xmlns="http://www.w3.org/2000/svg" class="inline h-5 w-5 mr-1" fill="none" viewBox="0 0 24 24" stroke="currentColor">
          <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M15 19l-7-7 7-7" />
        </svg>
        Volver al dashboard
      </router-link>
    </Card>
  </div>
</template>

<script setup>
import Card from '@/components/ui/Card.vue'
import { ref, onMounted } from 'vue';
import { useAuthStore } from '@/stores/auth';
import { useTheme } from '@/utils/useTheme';
import { useRouter } from 'vue-router';

const authStore = useAuthStore();
const loading = ref(true);
const error = ref(null);
const success = ref('');

const firstName = ref('');
const lastName = ref('');
const email = ref('');

// Theme selector logic
const { themes, currentTheme, applyTheme } = useTheme();
const selectedTheme = ref(currentTheme.value);

const router = useRouter();

const getEmail = () => {
  return authStore.user?.email || '';
};

const fetchProfile = async () => {
  loading.value = true;
  try {
    await authStore.fetchUserProfile();
    if (authStore.user) {
      if (authStore.user.user) {
        email.value = authStore.user.user.email || '';
        firstName.value = authStore.user.first_name || '';
        lastName.value = authStore.user.last_name || '';
      } else {
        firstName.value = authStore.user.first_name || '';
        lastName.value = authStore.user.last_name || '';
        email.value = authStore.user.email || getEmail();
      }
    } else {
      email.value = getEmail();
    }
    selectedTheme.value = currentTheme.value;
  } catch (err) {
    error.value = 'No se pudo cargar el perfil';
  } finally {
    loading.value = false;
  }
};

const onThemeChange = () => {
  applyTheme(selectedTheme.value);
};

onMounted(() => {
  fetchProfile();
});

const handleSubmit = async (e) => {
  e?.preventDefault?.();
  loading.value = true;
  error.value = null;
  success.value = '';

  try {
    const data = {
      email: email.value,
      first_name: firstName.value,
      last_name: lastName.value
    };
    if (authStore.isAuthenticated && authStore.updateProfile) {
      await authStore.updateProfile(data);
      await fetchProfile();
      success.value = '¡Perfil guardado exitosamente!';
    } else {
      success.value = '¡Preferencias guardadas!';
    }
  } catch (err) {
    error.value = err?.message || 'Error al actualizar el perfil';
  } finally {
    loading.value = false;
    setTimeout(() => { success.value = ''; }, 2500);
  }
};
</script>

<style scoped>
.fade-enter-active, .fade-leave-active {
  transition: opacity 0.5s;
}
.fade-enter-from, .fade-leave-to {
  opacity: 0;
}
</style>
