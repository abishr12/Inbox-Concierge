interface BucketManagerProps {
  buckets: string[]
  onAddBucket: (name: string) => void
  onRemoveBucket: (name: string) => void
}

export default function BucketManager({
  buckets,
  onAddBucket,
  onRemoveBucket,
}: BucketManagerProps): React.ReactElement {
  return (
    <div className="mb-6">
      <h2 className="text-xl font-semibold mb-3">Buckets</h2>
      <div className="flex flex-wrap gap-2">
        {buckets.map((bucket) => (
          <div
            key={bucket}
            className="flex items-center gap-2 px-3 py-1 bg-blue-100 rounded-full"
          >
            <span>{bucket}</span>
            <button
              onClick={() => onRemoveBucket(bucket)}
              className="text-red-600 hover:text-red-800"
            >
              ×
            </button>
          </div>
        ))}
        <button className="px-3 py-1 bg-gray-200 rounded-full hover:bg-gray-300">
          + Add
        </button>
      </div>
    </div>
  )
}
