"use client";

import type { Label } from "@/types";
import {
  startTransition,
  useEffect,
  useOptimistic,
  useRef,
  useState,
} from "react";
import { useAddBucket, useDeleteBucket } from "../hooks/useBucketMutations";

interface LabelsDropdownProps {
  labels: Label[];
  onRecategorize: () => Promise<void>;
}

export default function LabelsDropdown({
  labels,
  onRecategorize,
}: LabelsDropdownProps): React.ReactElement {
  const [isOpen, setIsOpen] = useState(false);
  const [isModalOpen, setIsModalOpen] = useState(false);
  const dropdownRef = useRef<HTMLDivElement>(null);

  const addBucket = useAddBucket(onRecategorize);
  const deleteBucket = useDeleteBucket(onRecategorize);
  const [optimisticLabels, setOptimisticLabels] = useOptimistic(
    labels,
    (currentLabels, labelIdToRemove: string) => {
      return currentLabels.filter((label) => label.id !== labelIdToRemove);
    },
  );

  useEffect(() => {
    const handleClickOutside = (event: MouseEvent): void => {
      if (
        dropdownRef.current &&
        !dropdownRef.current.contains(event.target as Node)
      ) {
        setIsOpen(false);
      }
    };

    if (isOpen) {
      document.addEventListener("mousedown", handleClickOutside);
    }

    return () => {
      document.removeEventListener("mousedown", handleClickOutside);
    };
  }, [isOpen]);

  const handleToggle = (): void => {
    setIsOpen(!isOpen);
  };

  const handleDelete = (labelId: string): void => {
    startTransition(async () => {
      setOptimisticLabels(labelId);

      try {
        await deleteBucket.mutateAsync(labelId);
      } catch (error) {
        // useOptimistic will automatically revert on error
        console.error("Failed to delete label:", error);
      }
    });
  };

  const handleAddNewClick = (): void => {
    setIsOpen(false);
    setIsModalOpen(true);
  };

  const handleModalClose = (): void => {
    setIsModalOpen(false);
  };

  const handleModalSubmit = (name: string, description: string): void => {
    setIsModalOpen(false);
    addBucket.mutate({ name, description });
  };

  return (
    <>
      <div className="relative" ref={dropdownRef}>
        <button
          onClick={handleToggle}
          className="flex items-center gap-1 px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-blue-500"
        >
          Labels
          <svg
            className={`w-4 h-4 transition-transform ${isOpen ? "rotate-180" : ""}`}
            fill="none"
            stroke="currentColor"
            viewBox="0 0 24 24"
          >
            <path
              strokeLinecap="round"
              strokeLinejoin="round"
              strokeWidth={2}
              d="M19 9l-7 7-7-7"
            />
          </svg>
        </button>

        {isOpen && (
          <div className="absolute left-0 mt-2 w-64 bg-white border border-gray-200 rounded-md shadow-lg z-20">
            <div className="px-4 py-2 border-b border-gray-200">
              <h3 className="text-sm font-semibold text-gray-700">Labels</h3>
            </div>

            <div className="max-h-64 overflow-y-auto">
              {optimisticLabels.length === 0 ? (
                <div className="px-4 py-3 text-sm text-gray-500 text-center">
                  No labels yet
                </div>
              ) : (
                <div className="py-1">
                  {optimisticLabels.map((label) => (
                    <div
                      key={label.id}
                      className="flex items-center justify-between px-4 py-2 hover:bg-gray-50"
                    >
                      <div className="flex items-center gap-2 flex-1">
                        <span
                          className="w-3 h-3 rounded-full flex-shrink-0"
                          style={{ backgroundColor: label.color }}
                        />
                        <span className="text-sm text-gray-900 truncate">
                          {label.name}
                        </span>
                      </div>
                      <button
                        onClick={() => handleDelete(label.id)}
                        disabled={deleteBucket.isPending}
                        className="ml-2 text-gray-400 hover:text-red-600 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
                        aria-label={`Delete ${label.name}`}
                      >
                        {deleteBucket.isPending ? (
                          <span className="inline-block animate-spin">⏳</span>
                        ) : (
                          "×"
                        )}
                      </button>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="border-t border-gray-200">
              <button
                onClick={handleAddNewClick}
                disabled={addBucket.isPending || deleteBucket.isPending}
                className="w-full px-4 py-2 text-left text-sm text-blue-600 hover:bg-blue-50 transition-colors disabled:opacity-50 disabled:cursor-not-allowed"
              >
                + Add New Label
              </button>
            </div>
          </div>
        )}
      </div>

      {isModalOpen && (
        <AddLabelModal
          isOpen={isModalOpen}
          onClose={handleModalClose}
          onSubmit={handleModalSubmit}
          isLoading={addBucket.isPending}
          error={addBucket.error?.message}
        />
      )}
    </>
  );
}

interface AddLabelModalProps {
  isOpen: boolean;
  onClose: () => void;
  onSubmit: (name: string, description: string) => void;
  isLoading?: boolean;
  error?: string;
}

function AddLabelModal({
  isOpen,
  onClose,
  onSubmit,
  isLoading = false,
  error: mutationError,
}: AddLabelModalProps): React.ReactElement | null {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [error, setError] = useState("");

  if (!isOpen) return null;

  const handleSubmit = (e: React.FormEvent): void => {
    e.preventDefault();

    if (!name.trim()) {
      setError("Name is required");
      return;
    }

    onSubmit(name.trim(), description.trim());
    setName("");
    setDescription("");
    setError("");
  };

  const handleClose = (): void => {
    setName("");
    setDescription("");
    setError("");
    onClose();
  };

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center bg-black/30">
      <div className="bg-white rounded-lg shadow-xl w-full max-w-md mx-4">
        <div className="flex items-center justify-between px-6 py-4 border-b border-gray-200">
          <h2 className="text-lg font-semibold text-gray-900">Add New Label</h2>
          <button
            onClick={handleClose}
            className="text-gray-400 hover:text-gray-600 transition-colors"
            aria-label="Close modal"
          >
            ×
          </button>
        </div>

        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {mutationError && (
            <div className="p-3 bg-red-50 border border-red-200 rounded-md">
              <p className="text-sm text-red-600">{mutationError}</p>
            </div>
          )}

          <div>
            <label
              htmlFor="label-name"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Name <span className="text-red-500">*</span>
            </label>
            <input
              id="label-name"
              type="text"
              value={name}
              onChange={(e) => {
                setName(e.target.value);
                setError("");
              }}
              disabled={isLoading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="e.g., Important"
            />
            {error && <p className="mt-1 text-sm text-red-600">{error}</p>}
          </div>

          <div>
            <label
              htmlFor="label-description"
              className="block text-sm font-medium text-gray-700 mb-1"
            >
              Description
            </label>
            <input
              id="label-description"
              type="text"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={isLoading}
              className="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-blue-500 disabled:bg-gray-100 disabled:cursor-not-allowed"
              placeholder="e.g., Urgent items requiring attention"
            />
          </div>

          <div className="flex justify-end gap-3 pt-4">
            <button
              type="button"
              onClick={handleClose}
              disabled={isLoading}
              className="px-4 py-2 text-sm font-medium text-gray-700 bg-white border border-gray-300 rounded-md hover:bg-gray-50 disabled:opacity-50 disabled:cursor-not-allowed"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={isLoading}
              className="px-4 py-2 text-sm font-medium text-white bg-blue-600 rounded-md hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed flex items-center gap-2"
            >
              {isLoading && (
                <span className="inline-block animate-spin">⏳</span>
              )}
              {isLoading ? "Adding..." : "Add Label"}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
