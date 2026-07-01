import './globals.css'
import { AuthProvider } from '@/context/AuthContext'
import { Toaster } from 'react-hot-toast'
import Navbar from '@/components/ui/Navbar'

export const metadata = {
    title: 'My Blog',
    description: 'A blog built with Django REST Framework and Next.js',
}

export default function RootLayout({ children }) {
    return (
        <html lang="en">
            <body>
                <AuthProvider>
                    <Navbar />
                    <main className="max-w-5xl mx-auto px-4 py-8">
                        {children}
                    </main>
                    <Toaster position="top-right" />
                </AuthProvider>
            </body>
        </html>
    )
}