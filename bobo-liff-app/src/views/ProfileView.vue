<template>
  <div class="font-sans">
    <div v-if="loading" class="fixed inset-0 z-50">
      <LoadingView message="Loading profile..."></LoadingView>
    </div>
    <div v-else-if="error" class="flex flex-col h-dvh max-w-md mx-auto bg-gray-50 items-center justify-center px-6 text-center">
      <p class="text-sm text-red-500">{{ error }}</p>
    </div>
    <div v-else class="flex flex-col h-dvh max-w-md mx-auto bg-gray-50 overflow-hidden">

      <!-- Header -->
      <div class="flex items-center gap-3 px-4 py-3 bg-white border-b border-gray-100 flex-shrink-0">
        <button class="w-9 h-9 rounded-full bg-gray-100 flex items-center justify-center" @click="$router.push('/')">
          <svg width="18" height="18" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M19 12H5M5 12l7-7M5 12l7 7"/></svg>
        </button>
        <div>
          <p class="text-xs font-semibold text-red-600 uppercase tracking-wider">Freelancer</p>
          <h2 class="text-lg font-bold text-gray-900 leading-tight">Profile</h2>
        </div>
      </div>

      <!-- Scrollable body -->
      <div class="flex-1 overflow-y-auto">
        <div class="p-4 space-y-3">

          <!-- Profile Hero -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm p-5 flex flex-col items-center gap-3">
            <div class="relative cursor-pointer group" @click="avatarModal = true">
              <div class="w-20 h-20 rounded-full bg-gray-100 overflow-hidden flex items-center justify-center">
                <img v-if="form.fl_profile_image_url" :src="form.fl_profile_image_url" class="w-full h-full object-cover" />
                <svg v-else width="36" height="36" viewBox="0 0 24 24" fill="none" stroke="#aaa" stroke-width="1.5"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
              </div>
              <div class="absolute inset-0 rounded-full bg-black/30 flex items-center justify-center opacity-0 group-hover:opacity-100 transition-opacity">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M23 19a2 2 0 0 1-2 2H3a2 2 0 0 1-2-2V8a2 2 0 0 1 2-2h4l2-3h6l2 3h4a2 2 0 0 1 2 2z"/><circle cx="12" cy="13" r="3"/></svg>
              </div>
              <div v-if="avatarUploading" class="absolute inset-0 rounded-full bg-white/70 flex items-center justify-center">
                <div class="w-5 h-5 border-2 border-red-600 border-t-transparent rounded-full animate-spin"></div>
              </div>
            </div>
            <input ref="avatarInput" type="file" accept="image/*" class="hidden" @change="uploadAvatar" />
            <div class="text-center">
              <h3 class="text-base font-bold text-gray-900">{{ form.fl_name }}</h3>
              <p class="text-sm text-gray-400">@{{ profile.fl_username }}</p>
            </div>
            <span :class="[BADGE_BASE, getVerifyStatusClass(profile.fl_verify_status)]">
              {{ formatVerifyStatus(profile.fl_verify_status) || 'Pending' }}
            </span>
            <div class="grid grid-cols-2 gap-4 w-full pt-2 border-t border-gray-100">
              <div class="text-center">
                <p class="text-lg font-bold text-gray-900 flex items-center justify-center gap-1">
                  {{ Number(profile.fl_rating_avg || 0).toFixed(1) }}
                  <svg width="14" height="14" viewBox="0 0 24 24" fill="#f9a825"><path d="M12 17.27L18.18 21l-1.64-7.03L22 9.24l-7.19-.61L12 2 9.19 8.63 2 9.24l5.46 4.73L5.82 21z"/></svg>
                </p>
                <p class="text-xs text-gray-400">Rating</p>
              </div>
              <div class="text-center">
                <p class="text-lg font-bold text-gray-900">{{ completedJobs }}</p>
                <p class="text-xs text-gray-400">Completed Jobs</p>
              </div>
            </div>
          </div>

          <!-- Edit Profile -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
              <div class="flex items-center gap-2">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><circle cx="12" cy="8" r="4"/><path d="M4 20c0-4 3.6-7 8-7s8 3 8 7"/></svg>
                <span class="text-sm font-semibold text-gray-700">Basic Information</span>
              </div>
              <div class="flex items-center gap-2">
                <button v-if="!isEditing"
                  class="flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 transition"
                  @click="isEditing = true">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  Edit
                </button>
                <button v-if="isEditing" class="px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 text-gray-500" @click="cancelEdit">Cancel</button>
                <button v-if="isEditing"
                  class="flex items-center gap-1 px-3 py-1.5 text-xs font-semibold rounded-lg bg-red-600 text-white disabled:opacity-60"
                  :disabled="saving" @click="saveProfile">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>
                  {{ saving ? 'Saving...' : 'Save' }}
                </button>
              </div>
            </div>
            <div v-if="saveSuccess" class="mx-4 mt-3 px-3 py-2 bg-green-50 border border-green-200 rounded-lg text-xs text-green-700">Profile updated!</div>
            <div v-if="saveError" class="mx-4 mt-3 px-3 py-2 bg-red-50 border border-red-200 rounded-lg text-xs text-red-600">{{ saveError }}</div>
            <div class="px-4 py-4 space-y-3">
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Username</label>
                <div class="relative">
                  <input :value="profile.fl_username" disabled class="w-full border border-gray-100 rounded-xl px-3 py-2.5 text-sm bg-gray-50 text-gray-400 cursor-not-allowed pr-14" />
                  <span class="absolute right-3 top-1/2 -translate-y-1/2 text-xs text-gray-300 uppercase">Fixed</span>
                </div>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Full Name <span class="text-red-400">*</span></label>
                <input v-model="form.fl_name" type="text" :disabled="!isEditing" placeholder="e.g. Somchai Jaidee"
                  class="w-full border rounded-xl px-3 py-2.5 text-sm transition"
                  :class="isEditing ? 'border-gray-200 bg-white focus:outline-none focus:border-red-400' : 'border-gray-100 bg-gray-50 text-gray-700 cursor-default'" />
              </div>
              <div class="grid grid-cols-2 gap-3">
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Phone <span class="text-red-400">*</span></label>
                  <input v-model="form.fl_phone" type="tel" :disabled="!isEditing" placeholder="0812345678"
                    class="w-full border rounded-xl px-3 py-2.5 text-sm transition"
                    :class="isEditing ? 'border-gray-200 bg-white focus:outline-none focus:border-red-400' : 'border-gray-100 bg-gray-50 text-gray-700 cursor-default'" />
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Date of Birth</label>
                  <input v-model="form.fl_date_of_birth" type="date" :disabled="!isEditing"
                    class="w-full border rounded-xl px-3 py-2.5 text-sm transition"
                    :class="isEditing ? 'border-gray-200 bg-white focus:outline-none focus:border-red-400' : 'border-gray-100 bg-gray-50 text-gray-700 cursor-default'" />
                </div>
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Email <span class="text-red-400">*</span></label>
                <input v-model="form.fl_email" type="email" :disabled="!isEditing" placeholder="somchai@email.com"
                  class="w-full border rounded-xl px-3 py-2.5 text-sm transition"
                  :class="isEditing ? 'border-gray-200 bg-white focus:outline-none focus:border-red-400' : 'border-gray-100 bg-gray-50 text-gray-700 cursor-default'" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Address</label>
                <input v-model="form.fl_address" type="text" :disabled="!isEditing" placeholder="e.g. Chiang Mai"
                  class="w-full border rounded-xl px-3 py-2.5 text-sm transition"
                  :class="isEditing ? 'border-gray-200 bg-white focus:outline-none focus:border-red-400' : 'border-gray-100 bg-gray-50 text-gray-700 cursor-default'" />
              </div>
              <div>
                <label class="block text-xs font-medium text-gray-500 mb-1">Bio</label>
                <textarea v-model="form.fl_bio" rows="3" :disabled="!isEditing" placeholder="Brief description..."
                  class="w-full border rounded-xl px-3 py-2.5 text-sm resize-none transition"
                  :class="isEditing ? 'border-gray-200 bg-white focus:outline-none focus:border-red-400' : 'border-gray-100 bg-gray-50 text-gray-700 cursor-default'"></textarea>
              </div>
            </div>
          </div>

          <!-- Languages & Areas -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
              <div class="flex items-center gap-2">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><circle cx="12" cy="12" r="10"/><path d="M2 12h20M12 2a15.3 15.3 0 0 1 4 10 15.3 15.3 0 0 1-4 10 15.3 15.3 0 0 1-4-10 15.3 15.3 0 0 1 4-10z"/></svg>
                <span class="text-sm font-semibold text-gray-700">Languages & Areas</span>
              </div>
              <button class="flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 transition" @click="isEditingTags = !isEditingTags">
                <svg v-if="!isEditingTags" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                {{ isEditingTags ? 'Done' : 'Edit' }}
              </button>
            </div>
            <div class="px-4 py-4 space-y-4">
              <div>
                <p class="text-xs font-medium text-gray-500 mb-2">Languages</p>
                <div class="flex flex-wrap gap-2">
                  <span v-for="lang in languages" :key="lang.language_id"
                    class="bg-indigo-50 text-indigo-700 text-xs font-medium px-3 py-1 rounded-full flex items-center gap-1.5">
                    {{ lang.language_name }}
                    <button v-if="isEditingTags" @click="removeLang(lang)" class="w-3.5 h-3.5 rounded-full bg-indigo-200 flex items-center justify-center">
                      <svg width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M18 6L6 18M6 6l12 12"/></svg>
                    </button>
                  </span>
                  <span v-if="!languages.length && !isEditingTags" class="text-xs text-gray-400 italic">No languages added.</span>
                </div>
                <div v-if="isEditingTags" class="flex gap-2 mt-2">
                  <input v-model="newLang" type="text" placeholder="e.g. English" class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-red-400" @keyup.enter="addLang" />
                  <button class="px-3 py-2 bg-red-600 text-white text-xs font-semibold rounded-xl disabled:opacity-60" :disabled="!newLang.trim() || addingLang" @click="addLang">{{ addingLang ? '...' : 'Add' }}</button>
                </div>
                <p v-if="langError" class="text-xs text-red-500 mt-1">{{ langError }}</p>
              </div>
              <div>
                <p class="text-xs font-medium text-gray-500 mb-2">Pickup Areas</p>
                <div class="flex flex-wrap gap-2">
                  <span v-for="area in pickupAreas" :key="area.area_id"
                    class="bg-cyan-50 text-cyan-700 text-xs font-medium px-3 py-1 rounded-full flex items-center gap-1.5">
                    {{ area.area_name }}
                    <button v-if="isEditingTags" @click="removeArea(area)" class="w-3.5 h-3.5 rounded-full bg-cyan-200 flex items-center justify-center">
                      <svg width="8" height="8" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="3"><path d="M18 6L6 18M6 6l12 12"/></svg>
                    </button>
                  </span>
                  <span v-if="!pickupAreas.length && !isEditingTags" class="text-xs text-gray-400 italic">No pickup areas added.</span>
                </div>
                <div v-if="isEditingTags" class="flex gap-2 mt-2">
                  <input v-model="newArea" type="text" placeholder="e.g. Chiang Mai" class="flex-1 border border-gray-200 rounded-xl px-3 py-2 text-sm focus:outline-none focus:border-red-400" @keyup.enter="addArea" />
                  <button class="px-3 py-2 bg-red-600 text-white text-xs font-semibold rounded-xl disabled:opacity-60" :disabled="!newArea.trim() || addingArea" @click="addArea">{{ addingArea ? '...' : 'Add' }}</button>
                </div>
                <p v-if="areaError" class="text-xs text-red-500 mt-1">{{ areaError }}</p>
              </div>
            </div>
          </div>

          <!-- Change PIN -->
          <button class="w-full bg-white rounded-2xl border border-gray-100 shadow-sm px-4 py-3.5 flex items-center justify-between active:bg-gray-50 transition"
            @click="$router.push('/profile/change-pin')">
            <div class="flex items-center gap-2">
              <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><rect x="5" y="11" width="14" height="10" rx="2"/><path d="M8 11V7a4 4 0 0 1 8 0v4"/></svg>
              <span class="text-sm font-semibold text-gray-700">Change PIN</span>
            </div>
            <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#9ca3af" stroke-width="2"><path d="M9 18l6-6-6-6"/></svg>
          </button>

          <!-- Vehicle -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
              <div class="flex items-center gap-2">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><rect x="1" y="8" width="15" height="10" rx="1.5"/><path d="M16 10l4 2v6h-4V10z"/><circle cx="5.5" cy="19.5" r="1.5"/><circle cx="13.5" cy="19.5" r="1.5"/><circle cx="19.5" cy="19.5" r="1.5"/></svg>
                <span class="text-sm font-semibold text-gray-700">Vehicle</span>
              </div>
              <div v-if="vehicle" class="flex items-center gap-2">
                <button v-if="!isEditingVehicle"
                  class="flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 transition"
                  @click="startEditVehicle">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                  Edit
                </button>
                <button v-if="isEditingVehicle" class="px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 text-gray-500" @click="cancelEditVehicle">Cancel</button>
                <button v-if="isEditingVehicle"
                  class="flex items-center gap-1 px-3 py-1.5 text-xs font-semibold rounded-lg bg-red-600 text-white disabled:opacity-60"
                  :disabled="savingVehicle" @click="saveVehicle">
                  <svg width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M20 6L9 17l-5-5"/></svg>
                  {{ savingVehicle ? 'Saving...' : 'Save' }}
                </button>
              </div>
            </div>
            <div v-if="vehicle">
              <div v-if="vehicleSaveSuccess" class="mx-4 mt-3 px-3 py-2 bg-green-50 border border-green-200 rounded-lg text-xs text-green-700">Saved!</div>
              <div v-if="vehicleSaveSuccess" class="mx-4 mt-3 px-3 py-2 bg-green-50 border border-green-200 rounded-lg text-xs text-green-700">Saved!</div>
              <div v-if="vehicleSaveError" class="mx-4 mt-3 px-3 py-2 bg-red-50 border border-red-200 rounded-lg text-xs text-red-600">{{ vehicleSaveError }}</div>
              <div class="px-4 py-4 space-y-3">
                <div v-for="vf in vehicleEditFields" :key="vf.key">
                  <label class="block text-xs font-medium text-gray-500 mb-1">{{ vf.label }}</label>
                  <input v-if="isEditingVehicle" v-model="vehicleForm[vf.key]" :type="vf.type || 'text'" :placeholder="vf.placeholder"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2.5 text-sm bg-white focus:outline-none focus:border-red-400" />
                  <p v-else class="text-sm text-gray-800 px-3 py-2.5 border border-gray-100 rounded-xl bg-gray-50">{{ vehicle[vf.key] || '—' }}</p>
                </div>
                <div>
                  <label class="block text-xs font-medium text-gray-500 mb-1">Type</label>
                  <p class="text-sm text-gray-800 px-3 py-2.5 border border-gray-100 rounded-xl bg-gray-50">{{ vehicle.fl_vehicle_type }}</p>
                </div>
              </div>
              <div v-if="vehicleImages.length" class="px-4 pb-3">
                <p class="text-xs font-medium text-gray-500 mb-2">Vehicle Photos</p>
                <div class="flex gap-2 overflow-x-auto pb-1">
                  <div v-for="img in vehicleImages" :key="img.fl_vehicle_image_id"
                    class="relative flex-shrink-0 w-24 h-24">
                    <img :src="img.fl_vehicle_image_url"
                      class="w-24 h-24 object-cover rounded-xl cursor-pointer active:opacity-80"
                      @click="!isEditingVehicle && (modalImage = img.fl_vehicle_image_url)" />
                    <div v-if="isEditingVehicle"
                      class="absolute inset-0 rounded-xl bg-black/40 flex items-center justify-center cursor-pointer"
                      @click="deleteVehicleImage(img)">
                      <svg width="22" height="22" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
                    </div>
                  </div>
                </div>
              </div>
              <div class="px-4 pb-4">
                <button class="flex items-center gap-1.5 text-xs text-red-600 font-medium bg-red-50 px-3 py-1.5 rounded-full" @click="triggerVehicleImageUpload">
                  <svg width="12" height="12" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><path d="M12 3v12"/></svg>
                  Add Vehicle Photo
                </button>
                <input ref="vehicleImageInput" type="file" accept="image/*" class="hidden" @change="uploadVehicleImage" />
              </div>
            </div>
            <div v-else class="px-4 py-4">
              <p class="text-xs text-gray-400 mb-3">No vehicle added yet.</p>
              <div class="grid grid-cols-2 gap-3">
                <div v-for="vf in vehicleEditFields" :key="vf.key">
                  <label class="block text-xs font-medium text-gray-500 mb-1">{{ vf.label }} <span class="text-red-400">*</span></label>
                  <input v-model="newVehicleForm[vf.key]" :type="vf.type || 'text'" :placeholder="vf.placeholder"
                    class="w-full border border-gray-200 rounded-xl px-3 py-2 text-sm bg-white focus:outline-none focus:border-red-400" />
                </div>
              </div>
              <p v-if="newVehicleError" class="text-xs text-red-500 mt-2">{{ newVehicleError }}</p>
              <button class="w-full mt-4 bg-red-600 text-white text-sm font-semibold py-3 rounded-xl disabled:opacity-60 flex items-center justify-center gap-2"
                :disabled="creatingVehicle" @click="createVehicle">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2.5"><path d="M12 5v14M5 12h14"/></svg>
                {{ creatingVehicle ? 'Adding...' : 'Add Vehicle' }}
              </button>
            </div>
          </div>

          <!-- Verification + Documents -->
          <div class="bg-white rounded-2xl border border-gray-100 shadow-sm overflow-hidden">
            <div class="flex items-center justify-between px-4 py-3 border-b border-gray-100">
              <div class="flex items-center gap-2">
                <svg width="14" height="14" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><path d="M9 12l2 2 4-4m5.618-4.016A11.955 11.955 0 0 1 12 2.944a11.955 11.955 0 0 1-8.618 3.04A12.02 12.02 0 0 0 3 9c0 5.591 3.824 10.29 9 11.622C17.176 19.29 21 14.591 21 9c0-1.847-.396-3.6-1.118-5.142z"/></svg>
                <span class="text-sm font-semibold text-gray-700">Verification</span>
              </div>
              <button class="flex items-center gap-1 px-3 py-1.5 text-xs font-medium rounded-lg border border-gray-200 text-gray-600 hover:bg-gray-50 transition" @click="docEditMode = !docEditMode">
                <svg v-if="!docEditMode" width="11" height="11" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M11 4H4a2 2 0 0 0-2 2v14a2 2 0 0 0 2 2h14a2 2 0 0 0 2-2v-7"/><path d="M18.5 2.5a2.121 2.121 0 0 1 3 3L12 15l-4 1 1-4 9.5-9.5z"/></svg>
                {{ docEditMode ? 'Done' : 'Edit' }}
              </button>
            </div>

            <!-- Verify status -->
            <div class="px-4 py-3 border-b border-gray-50 flex flex-wrap items-center gap-x-3 gap-y-1">
              <span class="text-xs font-medium text-gray-500">Status</span>
              <span class="text-xs font-semibold px-2.5 py-0.5 rounded-full uppercase"
                :class="[BADGE_BASE, getVerifyStatusClass(verifyInfo.fl_verify_status)]">
                {{ formatVerifyStatus(verifyInfo.fl_verify_status) || 'Pending' }}
              </span>
              <span v-if="verifyInfo.fl_verify_status === 'VERIFIED' && verifyInfo.fl_verified_at" class="text-xs text-gray-400">Verified {{ formatDate(verifyInfo.fl_verified_at) }}</span>
              <span v-else-if="verifyInfo.fl_submitted_at" class="text-xs text-gray-400">Submitted {{ formatDate(verifyInfo.fl_submitted_at) }}</span>
              <span v-if="verifyInfo.reviewed_by_name && verifyInfo.fl_verify_status === 'VERIFIED'" class="text-xs text-gray-400">By {{ verifyInfo.reviewed_by_name }}</span>
            </div>

            <!-- Documents label -->
            <div class="px-4 pt-3 pb-1">
              <p class="text-xs font-medium text-gray-500">Documents</p>
            </div>

            <!-- Documents list (1 per row) -->
            <div class="px-4 pb-4 space-y-2">
              <div v-if="!documents.length" class="py-4 text-center text-xs text-gray-400 italic">No documents found.</div>
              <div v-for="doc in documents" :key="doc.fl_doc_type"
                class="border border-gray-100 rounded-xl overflow-hidden bg-white cursor-pointer active:bg-gray-50 transition"
                @click="docEditMode ? triggerDocUpload(doc) : (doc.file_url ? openDocPreview(doc) : null)">
                <div class="flex items-center gap-3 p-3">

                  <!-- Thumbnail -->
                  <div class="w-14 h-14 rounded-lg bg-gray-50 flex-shrink-0 relative overflow-hidden">
                    <img v-if="doc.file_url && !doc.file_url.endsWith('.pdf')" :src="doc.file_url" class="w-full h-full object-cover" />
                    <div v-else-if="doc.file_url && doc.file_url.endsWith('.pdf')" class="w-full h-full flex items-center justify-center bg-red-50">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#dc2626" stroke-width="1.5"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"/><polyline points="14 2 14 8 20 8"/></svg>
                    </div>
                    <div v-else class="w-full h-full flex items-center justify-center">
                      <svg width="20" height="20" viewBox="0 0 24 24" fill="none" stroke="#d1d5db" stroke-width="1.5"><rect x="3" y="3" width="18" height="18" rx="2"/><circle cx="8.5" cy="8.5" r="1.5"/><polyline points="21 15 16 10 5 21"/></svg>
                    </div>
                    <div v-if="doc.uploading" class="absolute inset-0 bg-white/80 flex items-center justify-center">
                      <div class="w-4 h-4 border-2 border-red-600 border-t-transparent rounded-full animate-spin"></div>
                    </div>
                    <div v-if="docEditMode" class="absolute inset-0 bg-black/40 flex items-center justify-center rounded-lg">
                      <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="white" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><path d="M12 3v12"/></svg>
                    </div>
                  </div>

                  <!-- Info -->
                  <div class="flex-1 min-w-0">
                    <div class="flex items-center justify-between gap-2 mb-1">
                      <p class="text-sm font-semibold text-gray-800 truncate">{{ DOC_META[doc.fl_doc_type]?.label }}</p>
                      <span class="text-xs font-semibold px-2 py-0.5 rounded-full flex-shrink-0"
                        :class="docStatusStyle(doc.fl_doc_status).badge">
                        {{ doc.fl_doc_status || 'NOT UPLOADED' }}
                      </span>
                    </div>
                    <p class="text-xs text-gray-400">
                      {{ doc.fl_uploaded_at ? 'Last updated ' + formatDate(doc.fl_uploaded_at) : 'Not uploaded yet' }}
                    </p>
                    <p v-if="doc.reviewed_at && doc.fl_doc_status === 'APPROVED'" class="text-xs text-gray-400">
                      Verified {{ formatDate(doc.reviewed_at) }}{{ doc.reviewed_by_name ? ' by ' + doc.reviewed_by_name : '' }}
                    </p>
                    <p v-if="doc.fl_doc_status === 'REJECTED' && doc.reject_reason" class="text-xs text-red-400 mt-0.5">{{ doc.reject_reason }}</p>
                  </div>
                </div>
                <input :id="'doc-input-' + doc.fl_doc_type" type="file" accept="image/*,application/pdf" class="hidden" @change="(e) => uploadDocument(e, doc)" />
              </div>
            </div>
          </div>

        </div>
      </div>

      <!-- Avatar modal -->
      <div v-if="avatarModal" class="fixed inset-0 z-50 flex items-center justify-center bg-black/50" @click.self="avatarModal = false">
        <div class="bg-white rounded-2xl shadow-2xl w-72 overflow-hidden" @click.stop>
          <div class="px-5 py-4 border-b border-gray-100 flex items-center justify-between">
            <span class="text-sm font-semibold text-gray-900">Profile Photo</span>
            <button @click="avatarModal = false" class="text-gray-400">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
            </button>
          </div>
          <div class="py-1">
            <button :disabled="!form.fl_profile_image_url"
              class="w-full flex items-center gap-3 px-5 py-3 text-sm text-gray-700 hover:bg-gray-50 disabled:opacity-40 disabled:cursor-not-allowed"
              @click="viewAvatarFull">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><path d="M1 12s4-8 11-8 11 8 11 8-4 8-11 8-11-8-11-8z"/><circle cx="12" cy="12" r="3"/></svg>
              View Photo
            </button>
            <button class="w-full flex items-center gap-3 px-5 py-3 text-sm text-gray-700 hover:bg-gray-50"
              @click="avatarModal = false; avatarInput?.click()">
              <svg width="16" height="16" viewBox="0 0 24 24" fill="none" stroke="#6b7280" stroke-width="2"><path d="M21 15v4a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-4"/><polyline points="17 8 12 3 7 8"/><path d="M12 3v12"/></svg>
              Update Profile Photo
            </button>
          </div>
        </div>
      </div>

      <!-- Image modal -->
      <div v-if="modalImage" class="fixed inset-0 bg-black/80 z-50 flex items-center justify-center p-4" @click="modalImage = null">
        <button class="absolute top-4 right-4 text-white/80" @click="modalImage = null">
          <svg width="24" height="24" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2.5"><path d="M18 6L6 18M6 6l12 12"/></svg>
        </button>
        <img :src="modalImage" class="max-w-full max-h-full rounded-xl object-contain" />
      </div>
    </div>
  </div>
</template>

<script setup>
import LoadingView from './LoadingView.vue'
import { ref, reactive, onMounted } from 'vue'
import { getVerifyStatusClass, formatVerifyStatus, getDocStatusClass, BADGE_BASE } from '@/utils/statusClasses.js'

const props = defineProps({ user: Object })

const loading = ref(true)
const error = ref('')
const profile = ref({})
const vehicle = ref(null)
const vehicleImages = ref([])
const documents = ref([])
const languages = ref([])
const pickupAreas = ref([])
const verifyInfo = ref({})
const isEditingTags = ref(false)
const newLang = ref('')
const addingLang = ref(false)
const langError = ref('')
const newArea = ref('')
const addingArea = ref(false)
const areaError = ref('')
const completedJobs = ref(0)
const modalImage = ref(null)
const docEditMode = ref(false)

const isEditing = ref(false)
const saving = ref(false)
const saveError = ref('')
const saveSuccess = ref(false)

const isEditingVehicle = ref(false)
const savingVehicle = ref(false)
const vehicleSaveError = ref('')
const vehicleSaveSuccess = ref(false)
const vehicleForm = reactive({ fl_vehicle_brand: '', fl_vehicle_model: '', fl_vehicle_year: '', fl_vehicle_seat_capa: '', fl_vehicle_license_plate: '' })
const newVehicleForm = reactive({ fl_vehicle_brand: '', fl_vehicle_model: '', fl_vehicle_year: '', fl_vehicle_seat_capa: '', fl_vehicle_license_plate: '' })
const creatingVehicle = ref(false)
const newVehicleError = ref('')
const vehicleFormSnapshot = reactive({})

const avatarModal = ref(false)
const avatarInput = ref(null)
const avatarUploading = ref(false)
const vehicleImageInput = ref(null)

const API_BASE = import.meta.env.VITE_FASTAPI_URL || 'http://localhost:8000'
const HEADERS = { 'ngrok-skip-browser-warning': 'true' }

const form = reactive({ fl_name: '', fl_email: '', fl_phone: '', fl_address: '', fl_bio: '', fl_date_of_birth: '', fl_profile_image_url: '' })
const formSnapshot = reactive({})

const vehicleEditFields = [
  { key: 'fl_vehicle_brand',         label: 'Brand',         placeholder: 'e.g. Toyota',   type: 'text' },
  { key: 'fl_vehicle_model',         label: 'Model',         placeholder: 'e.g. Commuter', type: 'text' },
  { key: 'fl_vehicle_year',          label: 'Year',          placeholder: '2020',           type: 'number' },
  { key: 'fl_vehicle_seat_capa',     label: 'Seats (9-13)', placeholder: '10',             type: 'number' },
  { key: 'fl_vehicle_license_plate', label: 'License Plate', placeholder: 'กข 1234',       type: 'text' },
]

const DOC_META = {
  PERSONAL_ID:           { label: 'ID Card' },
  DRIVER_LICENSE:        { label: 'Driver License' },
  PUBLIC_DRIVER_LICENSE: { label: 'Public Driver License' },
  VEHICLE_REGISTRATION:  { label: 'Vehicle Registration' },
  VEHICLE_INSPECTION:    { label: 'Vehicle Inspection' },
}

onMounted(async () => {
  const flId = props.user?.fl_id
  if (!flId) { error.value = 'User not found. Please login again.'; loading.value = false; return }
  try {
    const [profileRes, vehicleRes, vehicleImgRes, docRes, jobsRes, verifyRes, langRes, areaRes] = await Promise.all([
      fetch(`${API_BASE}/freelancers/${flId}`, { headers: HEADERS }),
      fetch(`${API_BASE}/fl-vehicle?fl_id=${flId}`, { headers: HEADERS }),
      fetch(`${API_BASE}/fl-vehicle-images?fl_id=${flId}`, { headers: HEADERS }),
      fetch(`${API_BASE}/fl-documents?fl_id=${flId}`, { headers: HEADERS }),
      fetch(`${API_BASE}/jobs?fl_id=${flId}&status=COMPLETED&limit=200`, { headers: HEADERS }),
      fetch(`${API_BASE}/fl-verification?fl_id=${flId}&is_latest=true&status=&limit=1`, { headers: HEADERS }),
      fetch(`${API_BASE}/fl-languages?fl_id=${flId}`, { headers: HEADERS }),
      fetch(`${API_BASE}/fl-pickup-areas?fl_id=${flId}`, { headers: HEADERS }),
    ])
    const [profileData, vehicleData, vehicleImgData, docData, jobsData, verifyData, langData, areaData] = await Promise.all([
      profileRes.json(), vehicleRes.json(), vehicleImgRes.json(), docRes.json(),
      jobsRes.json(), verifyRes.json(), langRes.json(), areaRes.json()
    ])
    profile.value = profileData
    form.fl_name = profileData.fl_name || ''
    form.fl_email = profileData.fl_email || ''
    form.fl_phone = profileData.fl_phone || ''
    form.fl_address = profileData.fl_address || ''
    form.fl_bio = profileData.fl_bio || ''
    form.fl_date_of_birth = profileData.fl_date_of_birth ? profileData.fl_date_of_birth.split('T')[0] : ''
    form.fl_profile_image_url = profileData.fl_profile_image_url || ''
    Object.assign(formSnapshot, { ...form })
    vehicle.value       = vehicleData.items?.[0]   || null
    vehicleImages.value = vehicleImgData.items      || []
    documents.value     = docData.items             || []
    verifyInfo.value    = verifyData.items?.[0]     || {}
    languages.value     = langData.items            || []
    pickupAreas.value   = areaData.items            || []
    completedJobs.value = jobsData.total ?? (jobsData.items?.length ?? 0)
  } catch (e) { error.value = `Failed to load profile: ${e.message}` }
  finally { loading.value = false }
})

function cancelEdit() { Object.assign(form, formSnapshot); isEditing.value = false; saveError.value = '' }

async function saveProfile() {
  saving.value = true; saveError.value = ''; saveSuccess.value = false
  try {
    const res = await fetch(`${API_BASE}/freelancers/${props.user.fl_id}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json', ...HEADERS },
      body: JSON.stringify({ fl_name: form.fl_name, fl_email: form.fl_email, fl_phone: form.fl_phone, fl_address: form.fl_address, fl_bio: form.fl_bio, fl_date_of_birth: form.fl_date_of_birth || null, fl_profile_image_url: form.fl_profile_image_url || null }),
    })
    if (!res.ok) { const d = await res.json(); saveError.value = d.detail || 'Failed to save.'; return }
    Object.assign(formSnapshot, { ...form }); profile.value = { ...profile.value, ...form }
    isEditing.value = false; saveSuccess.value = true; setTimeout(() => saveSuccess.value = false, 3000)
  } catch { saveError.value = 'Unable to connect.' }
  finally { saving.value = false }
}

function startEditVehicle() {
  if (!vehicle.value) return
  Object.assign(vehicleForm, {
    fl_vehicle_brand: vehicle.value.fl_vehicle_brand || '',
    fl_vehicle_model: vehicle.value.fl_vehicle_model || '',
    fl_vehicle_year: vehicle.value.fl_vehicle_year || '',
    fl_vehicle_seat_capa: vehicle.value.fl_vehicle_seat_capa || '',
    fl_vehicle_license_plate: vehicle.value.fl_vehicle_license_plate || '',
  })
  Object.assign(vehicleFormSnapshot, { ...vehicleForm })
  isEditingVehicle.value = true
}

function cancelEditVehicle() { Object.assign(vehicleForm, vehicleFormSnapshot); isEditingVehicle.value = false; vehicleSaveError.value = '' }

async function saveVehicle() {
  savingVehicle.value = true; vehicleSaveError.value = ''; vehicleSaveSuccess.value = false
  try {
    const res = await fetch(`${API_BASE}/fl-vehicle/${vehicle.value.fl_vehicle_id}`, {
      method: 'PUT', headers: { 'Content-Type': 'application/json', ...HEADERS },
      body: JSON.stringify({ fl_vehicle_brand: vehicleForm.fl_vehicle_brand, fl_vehicle_model: vehicleForm.fl_vehicle_model, fl_vehicle_year: Number(vehicleForm.fl_vehicle_year) || null, fl_vehicle_seat_capa: Number(vehicleForm.fl_vehicle_seat_capa) || null, fl_vehicle_license_plate: vehicleForm.fl_vehicle_license_plate }),
    })
    if (!res.ok) { const d = await res.json(); vehicleSaveError.value = d.detail || 'Failed to save.'; return }
    vehicle.value = { ...vehicle.value, ...vehicleForm }
    Object.assign(vehicleFormSnapshot, { ...vehicleForm })
    isEditingVehicle.value = false; vehicleSaveSuccess.value = true; setTimeout(() => vehicleSaveSuccess.value = false, 3000)
  } catch { vehicleSaveError.value = 'Unable to connect.' }
  finally { savingVehicle.value = false }
}

function viewAvatarFull() { avatarModal.value = false; modalImage.value = form.fl_profile_image_url }

async function uploadAvatar(e) {
  const file = e.target.files[0]; if (!file) return
  avatarUploading.value = true
  try {
    const fd = new FormData(); fd.append('file', file)
    const res = await fetch(`${API_BASE}/upload/freelancer-profile`, { method: 'POST', headers: HEADERS, body: fd })
    if (!res.ok) throw new Error('Upload failed')
    const data = await res.json()
    const url = data.url || data.file_url || data.public_url
    form.fl_profile_image_url = url
    await fetch(`${API_BASE}/freelancers/${props.user.fl_id}`, { method: 'PUT', headers: { 'Content-Type': 'application/json', ...HEADERS }, body: JSON.stringify({ fl_profile_image_url: url }) })
  } catch { saveError.value = 'Failed to upload photo.' }
  finally { avatarUploading.value = false; e.target.value = '' }
}

function triggerVehicleImageUpload() { vehicleImageInput.value?.click() }

async function uploadVehicleImage(e) {
  const file = e.target.files[0]; if (!file || !vehicle.value) return
  try {
    const fd = new FormData(); fd.append('file', file)
    const res = await fetch(`${API_BASE}/fl-vehicle/${vehicle.value.fl_vehicle_id}/images`, { method: 'POST', headers: HEADERS, body: fd })
    if (!res.ok) throw new Error('Upload failed')
    const data = await res.json(); vehicleImages.value.unshift(data)
  } catch { vehicleSaveError.value = 'Failed to upload vehicle image.' }
  finally { e.target.value = '' }
}

function triggerDocUpload(doc) { document.getElementById('doc-input-' + doc.fl_doc_type)?.click() }

function openDocPreview(doc) {
  if (!doc.file_url) return
  if (doc.file_url.endsWith('.pdf')) { window.open(doc.file_url, '_blank') }
  else { modalImage.value = doc.file_url }
}

async function uploadDocument(e, doc) {
  const file = e.target.files[0]; if (!file) return
  const idx = documents.value.findIndex(d => d.fl_doc_type === doc.fl_doc_type)
  if (idx === -1) return
  documents.value[idx] = { ...documents.value[idx], uploading: true }
  try {
    const fd = new FormData(); fd.append('file', file)
    const res = await fetch(`${API_BASE}/fl-documents/${props.user.fl_id}/upload?doc_type=${doc.fl_doc_type}`, { method: 'POST', headers: HEADERS, body: fd })
    if (!res.ok) { const err = await res.json(); throw new Error(err.detail || 'Upload failed') }
    const data = await res.json()
    documents.value[idx] = { ...documents.value[idx], file_url: data.file_url, fl_doc_status: 'PENDING', fl_uploaded_at: new Date().toISOString(), uploading: false }
  } catch (err) {
    console.error('Failed to upload:', err.message)
    documents.value[idx] = { ...documents.value[idx], uploading: false }
  } finally { e.target.value = '' }
}

async function addLang() {
  if (!newLang.value.trim()) return
  addingLang.value = true; langError.value = ''
  try {
    const res = await fetch(`${API_BASE}/fl-languages`, { method: 'POST', headers: { 'Content-Type': 'application/json', ...HEADERS }, body: JSON.stringify({ fl_id: props.user.fl_id, language_name: newLang.value.trim() }) })
    const data = await res.json()
    if (!res.ok) { langError.value = data.detail || 'Failed to add.'; return }
    languages.value.push(data); newLang.value = ''
  } catch { langError.value = 'Cannot connect.' }
  finally { addingLang.value = false }
}

async function removeLang(lang) {
  try {
    await fetch(`${API_BASE}/fl-languages/${props.user.fl_id}/${lang.language_id}`, { method: 'DELETE', headers: HEADERS })
    languages.value = languages.value.filter(l => l.language_id !== lang.language_id)
  } catch { langError.value = 'Failed to remove language.' }
}

async function addArea() {
  if (!newArea.value.trim()) return
  addingArea.value = true; areaError.value = ''
  try {
    const res = await fetch(`${API_BASE}/fl-pickup-areas`, { method: 'POST', headers: { 'Content-Type': 'application/json', ...HEADERS }, body: JSON.stringify({ fl_id: props.user.fl_id, area_name: newArea.value.trim() }) })
    const data = await res.json()
    if (!res.ok) { areaError.value = data.detail || 'Failed to add.'; return }
    pickupAreas.value.push(data); newArea.value = ''
  } catch { areaError.value = 'Cannot connect.' }
  finally { addingArea.value = false }
}

async function removeArea(area) {
  try {
    await fetch(`${API_BASE}/fl-pickup-areas/${props.user.fl_id}/${area.area_id}`, { method: 'DELETE', headers: HEADERS })
    pickupAreas.value = pickupAreas.value.filter(a => a.area_id !== area.area_id)
  } catch { areaError.value = 'Failed to remove area.' }
}

async function createVehicle() {
  const { fl_vehicle_brand, fl_vehicle_model, fl_vehicle_year, fl_vehicle_seat_capa, fl_vehicle_license_plate } = newVehicleForm
  if (!fl_vehicle_brand || !fl_vehicle_model || !fl_vehicle_year || !fl_vehicle_seat_capa || !fl_vehicle_license_plate) { newVehicleError.value = 'Please fill in all fields.'; return }
  creatingVehicle.value = true; newVehicleError.value = ''
  try {
    const res = await fetch(`${API_BASE}/fl-vehicle?fl_id=${props.user.fl_id}`, { method: 'POST', headers: { 'Content-Type': 'application/json', ...HEADERS }, body: JSON.stringify({ fl_vehicle_brand, fl_vehicle_model, fl_vehicle_year: Number(fl_vehicle_year), fl_vehicle_seat_capa: Number(fl_vehicle_seat_capa), fl_vehicle_license_plate }) })
    const data = await res.json()
    if (!res.ok) { newVehicleError.value = data.detail || 'Failed to add vehicle.'; return }
    vehicle.value = data
  } catch { newVehicleError.value = 'Cannot connect to server.' }
  finally { creatingVehicle.value = false }
}

async function deleteVehicleImage(img) {
  try {
    const res = await fetch(`${API_BASE}/fl-vehicle/${vehicle.value.fl_vehicle_id}/images/${img.fl_vehicle_image_id}`, {
      method: 'DELETE', headers: HEADERS
    })
    if (!res.ok) throw new Error('Failed to delete')
    vehicleImages.value = vehicleImages.value.filter(i => i.fl_vehicle_image_id !== img.fl_vehicle_image_id)
  } catch { vehicleSaveError.value = 'Failed to delete image.' }
}

function formatDate(dateStr) {
  if (!dateStr) return '—'
  return new Date(dateStr).toLocaleDateString('en-GB', { day: '2-digit', month: 'short', year: 'numeric' })
}

function docStatusStyle(status) {
  return { badge: getDocStatusClass(status) }
}
</script>