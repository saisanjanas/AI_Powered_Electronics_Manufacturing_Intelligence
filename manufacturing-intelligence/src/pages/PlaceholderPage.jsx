import DashboardLayout from '../components/layout/DashboardLayout'

export default function PlaceholderPage({
  title,
  breadcrumb,
  description,
  image,
  images = [],
}) {
  const allImages = image ? [image, ...images] : images

  return (
    <DashboardLayout title={title} breadcrumb={breadcrumb}>
      <div className="mb-6">
        <h2 className="text-lg font-semibold text-ink">
          {title}
        </h2>

        {description && (
          <p className="text-sm text-ink-muted mt-1">
            {description}
          </p>
        )}
      </div>

      {allImages.length > 0 ? (
        <div className="space-y-6">
          {allImages.map((img, index) => (
            <div
              key={img}
              className="rounded-card border border-surface-border bg-white overflow-hidden"
            >
              <img
                src={img}
                alt={`${title} ${index + 1}`}
                className="w-full h-auto block"
              />
            </div>
          ))}
        </div>
      ) : (
        <div className="rounded-card border border-surface-border bg-white p-6">
          <p className="text-sm font-semibold text-ink">
            {title}
          </p>

          <p className="text-sm text-ink-muted mt-2">
            This section is currently under development.
          </p>
        </div>
      )}
    </DashboardLayout>
  )
}