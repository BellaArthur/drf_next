export default function Button({ children, loading, variant = 'primary', ...props }) {
    const base = 'px-4 py-2 rounded-md font-medium transition disabled:opacity-50'
    const variants = {
        primary:   'bg-blue-600 text-white hover:bg-blue-700',
        secondary: 'bg-gray-200 text-gray-800 hover:bg-gray-300',
        danger:    'bg-red-600 text-white hover:bg-red-700',
    }

    return (
        <button
            {...props}
            disabled={loading || props.disabled}
            className={`${base} ${variants[variant]} ${props.className || ''}`}
        >
            {loading ? 'Loading...' : children}
        </button>
    )
}