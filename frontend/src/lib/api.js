import api from './axios'

// ─── Auth ─────────────────────────────────────────────────────────────────────

export const authAPI = {

    register: (data) =>
        api.post('/auth/register/', data),

    login: (data) =>
        api.post('/auth/login/', data),

    logout: (refresh) =>
        api.post('/auth/logout/', { refresh }),

    refreshToken: (refresh) =>
        api.post('/auth/token/refresh/', { refresh }),

    getMe: () =>
        api.get('/auth/me/'),

    updateMe: (data) =>
        api.patch('/auth/me/', data, {
            headers: { 'Content-Type': 'multipart/form-data' }
        }),

    changePassword: (data) =>
        api.post('/auth/change-password/', data),
}

// ─── Posts ────────────────────────────────────────────────────────────────────

export const postsAPI = {

    list: (params) =>
        api.get('/blog/posts/', { params }),

    get: (slug) =>
        api.get(`/blog/posts/${slug}/`),

    create: (data) =>
        api.post('/blog/posts/', data, {
            headers: { 'Content-Type': 'multipart/form-data' }
        }),

    update: (slug, data) =>
        api.patch(`/blog/posts/${slug}/`, data, {
            headers: { 'Content-Type': 'multipart/form-data' }
        }),

    delete: (slug) =>
        api.delete(`/blog/posts/${slug}/`),

    toggleLike: (slug) =>
        api.post(`/blog/posts/${slug}/like/`),
}

// ─── Comments ─────────────────────────────────────────────────────────────────

export const commentsAPI = {

    list: (slug, params) =>
        api.get(`/blog/posts/${slug}/comments/`, { params }),

    create: (slug, data) =>
        api.post(`/blog/posts/${slug}/comments/`, data),

    update: (slug, id, data) =>
        api.patch(`/blog/posts/${slug}/comments/${id}/`, data),

    delete: (slug, id) =>
        api.delete(`/blog/posts/${slug}/comments/${id}/`),
}

// ─── Categories ───────────────────────────────────────────────────────────────

export const categoriesAPI = {

    list: () =>
        api.get('/blog/categories/'),

    get: (slug) =>
        api.get(`/blog/categories/${slug}/`),
}

// ─── Tags ─────────────────────────────────────────────────────────────────────

export const tagsAPI = {

    list: () =>
        api.get('/blog/tags/'),

    get: (slug) =>
        api.get(`/blog/tags/${slug}/`),
}