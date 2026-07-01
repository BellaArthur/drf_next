'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useAuth } from '@/context/AuthContext'
import Input from '@/components/ui/Input'
import Button from '@/components/ui/Button'

export default function RegisterPage() {
    const { register } = useAuth()
    const [loading, setLoading] = useState(false)
    const [errors, setErrors]   = useState({})
    const [form, setForm] = useState({
        email: '',
        first_name: '',
        last_name: '',
        password: '',
        password2: '',
    })

    const handleChange = (e) => {
        setForm({ ...form, [e.target.name]: e.target.value })
    }

    const handleSubmit = async (e) => {
        e.preventDefault()
        setErrors({})
        setLoading(true)
        try {
            await register(form)
        } catch (err) {
            setErrors(err.response?.data?.errors || {})
        } finally {
            setLoading(false)
        }
    }

    return (
        <div className="max-w-md mx-auto mt-16 p-6 bg-white rounded-lg shadow">
            <h1 className="text-2xl font-bold mb-6">Create an account</h1>

            <form onSubmit={handleSubmit}>
                <Input
                    label="First name"
                    name="first_name"
                    value={form.first_name}
                    onChange={handleChange}
                    error={errors.first_name?.[0]}
                    required
                />
                <Input
                    label="Last name"
                    name="last_name"
                    value={form.last_name}
                    onChange={handleChange}
                    error={errors.last_name?.[0]}
                    required
                />
                <Input
                    label="Email"
                    name="email"
                    type="email"
                    value={form.email}
                    onChange={handleChange}
                    error={errors.email?.[0]}
                    required
                />
                <Input
                    label="Password"
                    name="password"
                    type="password"
                    value={form.password}
                    onChange={handleChange}
                    error={errors.password?.[0]}
                    required
                />
                <Input
                    label="Confirm password"
                    name="password2"
                    type="password"
                    value={form.password2}
                    onChange={handleChange}
                    error={errors.password2?.[0]}
                    required
                />

                <Button type="submit" loading={loading} className="w-full">
                    Register
                </Button>
            </form>

            <p className="text-sm text-gray-600 mt-4">
                Already have an account?{' '}
                <Link href="/login" className="text-blue-600 hover:underline">
                    Login
                </Link>
            </p>
        </div>
    )
}