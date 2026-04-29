-- ============================================================
-- 1. admin_logs → admins
-- ============================================================
SELECT 'admin_logs.admin_id orphan' AS check_name, COUNT(*) AS broken_count
FROM admin_logs al
LEFT JOIN admins a ON al.admin_id = a.admin_id
WHERE a.admin_id IS NULL

UNION ALL

-- ============================================================
-- 2. fl_bank_accounts → freelancers
-- ============================================================
SELECT 'fl_bank_accounts.fl_id orphan', COUNT(*)
FROM fl_bank_accounts fb
LEFT JOIN freelancers f ON fb.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 3. em_bank_accounts → employers
-- ============================================================
SELECT 'em_bank_accounts.em_id orphan', COUNT(*)
FROM em_bank_accounts eb
LEFT JOIN employers e ON eb.em_id = e.em_id
WHERE e.em_id IS NULL

UNION ALL

-- ============================================================
-- 4. fl_vehicle → freelancers
-- ============================================================
SELECT 'fl_vehicle.fl_id orphan', COUNT(*)
FROM fl_vehicle fv
LEFT JOIN freelancers f ON fv.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 5. fl_vehicle_images → fl_vehicle
-- ============================================================
SELECT 'fl_vehicle_images.fl_vehicle_id orphan', COUNT(*)
FROM fl_vehicle_images fvi
LEFT JOIN fl_vehicle fv ON fvi.fl_vehicle_id = fv.fl_vehicle_id
WHERE fv.fl_vehicle_id IS NULL

UNION ALL

-- ============================================================
-- 6. fl_languages → freelancers
-- ============================================================
SELECT 'fl_languages.fl_id orphan', COUNT(*)
FROM fl_languages fl
LEFT JOIN freelancers f ON fl.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 7. fl_pickup_areas → freelancers
-- ============================================================
SELECT 'fl_pickup_areas.fl_id orphan', COUNT(*)
FROM fl_pickup_areas fp
LEFT JOIN freelancers f ON fp.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 8. fl_availability → freelancers
-- ============================================================
SELECT 'fl_availability.fl_id orphan', COUNT(*)
FROM fl_availability fa
LEFT JOIN freelancers f ON fa.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 9. fl_documents → freelancers
-- ============================================================
SELECT 'fl_documents.fl_id orphan', COUNT(*)
FROM fl_documents fd
LEFT JOIN freelancers f ON fd.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 10. fl_documents → fl_vehicle (nullable)
-- ============================================================
SELECT 'fl_documents.fl_vehicle_id orphan', COUNT(*)
FROM fl_documents fd
LEFT JOIN fl_vehicle fv ON fd.fl_vehicle_id = fv.fl_vehicle_id
WHERE fd.fl_vehicle_id IS NOT NULL AND fv.fl_vehicle_id IS NULL

UNION ALL

-- ============================================================
-- 11. fl_documents → admins (nullable reviewed_by)
-- ============================================================
SELECT 'fl_documents.reviewed_by orphan', COUNT(*)
FROM fl_documents fd
LEFT JOIN admins a ON fd.reviewed_by = a.admin_id
WHERE fd.reviewed_by IS NOT NULL AND a.admin_id IS NULL

UNION ALL

-- ============================================================
-- 12. fl_verification → freelancers
-- ============================================================
SELECT 'fl_verification.fl_id orphan', COUNT(*)
FROM fl_verification fv
LEFT JOIN freelancers f ON fv.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 13. fl_verification → admins (nullable)
-- ============================================================
SELECT 'fl_verification.reviewed_by orphan', COUNT(*)
FROM fl_verification fv
LEFT JOIN admins a ON fv.reviewed_by = a.admin_id
WHERE fv.reviewed_by IS NOT NULL AND a.admin_id IS NULL

UNION ALL

-- ============================================================
-- 14. em_documents → employers
-- ============================================================
SELECT 'em_documents.em_id orphan', COUNT(*)
FROM em_documents ed
LEFT JOIN employers e ON ed.em_id = e.em_id
WHERE e.em_id IS NULL

UNION ALL

-- ============================================================
-- 15. em_documents → admins (nullable)
-- ============================================================
SELECT 'em_documents.reviewed_by orphan', COUNT(*)
FROM em_documents ed
LEFT JOIN admins a ON ed.reviewed_by = a.admin_id
WHERE ed.reviewed_by IS NOT NULL AND a.admin_id IS NULL

UNION ALL

-- ============================================================
-- 16. em_verification → employers
-- ============================================================
SELECT 'em_verification.em_id orphan', COUNT(*)
FROM em_verification ev
LEFT JOIN employers e ON ev.em_id = e.em_id
WHERE e.em_id IS NULL

UNION ALL

-- ============================================================
-- 17. em_verification → admins (nullable)
-- ============================================================
SELECT 'em_verification.reviewed_by orphan', COUNT(*)
FROM em_verification ev
LEFT JOIN admins a ON ev.reviewed_by = a.admin_id
WHERE ev.reviewed_by IS NOT NULL AND a.admin_id IS NULL

UNION ALL

-- ============================================================
-- 18. jobs → employers
-- ============================================================
SELECT 'jobs.em_id orphan', COUNT(*)
FROM jobs j
LEFT JOIN employers e ON j.em_id = e.em_id
WHERE e.em_id IS NULL

UNION ALL

-- ============================================================
-- 19. jobs → freelancers (nullable selected_fl_id)
-- ============================================================
SELECT 'jobs.selected_fl_id orphan', COUNT(*)
FROM jobs j
LEFT JOIN freelancers f ON j.selected_fl_id = f.fl_id
WHERE j.selected_fl_id IS NOT NULL AND f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 20. job_required_languages → jobs
-- ============================================================
SELECT 'job_required_languages.job_id orphan', COUNT(*)
FROM job_required_languages jrl
LEFT JOIN jobs j ON jrl.job_id = j.job_id
WHERE j.job_id IS NULL

UNION ALL

-- ============================================================
-- 21. job_itineraries → jobs
-- ============================================================
SELECT 'job_itineraries.job_id orphan', COUNT(*)
FROM job_itineraries ji
LEFT JOIN jobs j ON ji.job_id = j.job_id
WHERE j.job_id IS NULL

UNION ALL

-- ============================================================
-- 22. job_passengers → jobs
-- ============================================================
SELECT 'job_passengers.job_id orphan', COUNT(*)
FROM job_passengers jp
LEFT JOIN jobs j ON jp.job_id = j.job_id
WHERE j.job_id IS NULL

UNION ALL

-- ============================================================
-- 23. job_expenses → jobs
-- ============================================================
SELECT 'job_expenses.job_id orphan', COUNT(*)
FROM job_expenses je
LEFT JOIN jobs j ON je.job_id = j.job_id
WHERE j.job_id IS NULL

UNION ALL

-- ============================================================
-- 24. job_applications → jobs
-- ============================================================
SELECT 'job_applications.job_id orphan', COUNT(*)
FROM job_applications ja
LEFT JOIN jobs j ON ja.job_id = j.job_id
WHERE j.job_id IS NULL

UNION ALL

-- ============================================================
-- 25. job_applications → freelancers
-- ============================================================
SELECT 'job_applications.fl_id orphan', COUNT(*)
FROM job_applications ja
LEFT JOIN freelancers f ON ja.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 26. job_payments → jobs
-- ============================================================
SELECT 'job_payments.job_id orphan', COUNT(*)
FROM job_payments jp
LEFT JOIN jobs j ON jp.job_id = j.job_id
WHERE j.job_id IS NULL

UNION ALL

-- ============================================================
-- 27. job_payments → employers
-- ============================================================
SELECT 'job_payments.em_id orphan', COUNT(*)
FROM job_payments jp
LEFT JOIN employers e ON jp.em_id = e.em_id
WHERE e.em_id IS NULL

UNION ALL

-- ============================================================
-- 28. job_payments → freelancers
-- ============================================================
SELECT 'job_payments.fl_id orphan', COUNT(*)
FROM job_payments jp
LEFT JOIN freelancers f ON jp.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 29. fl_reviews → jobs
-- ============================================================
SELECT 'fl_reviews.job_id orphan', COUNT(*)
FROM fl_reviews fr
LEFT JOIN jobs j ON fr.job_id = j.job_id
WHERE j.job_id IS NULL

UNION ALL

-- ============================================================
-- 30. fl_reviews → employers
-- ============================================================
SELECT 'fl_reviews.em_id orphan', COUNT(*)
FROM fl_reviews fr
LEFT JOIN employers e ON fr.em_id = e.em_id
WHERE e.em_id IS NULL

UNION ALL

-- ============================================================
-- 31. fl_reviews → freelancers
-- ============================================================
SELECT 'fl_reviews.fl_id orphan', COUNT(*)
FROM fl_reviews fr
LEFT JOIN freelancers f ON fr.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 32. em_reviews → jobs
-- ============================================================
SELECT 'em_reviews.job_id orphan', COUNT(*)
FROM em_reviews er
LEFT JOIN jobs j ON er.job_id = j.job_id
WHERE j.job_id IS NULL

UNION ALL

-- ============================================================
-- 33. em_reviews → freelancers
-- ============================================================
SELECT 'em_reviews.fl_id orphan', COUNT(*)
FROM em_reviews er
LEFT JOIN freelancers f ON er.fl_id = f.fl_id
WHERE f.fl_id IS NULL

UNION ALL

-- ============================================================
-- 34. em_reviews → employers
-- ============================================================
SELECT 'em_reviews.em_id orphan', COUNT(*)
FROM em_reviews er
LEFT JOIN employers e ON er.em_id = e.em_id
WHERE e.em_id IS NULL

UNION ALL

-- ============================================================
-- 35. jobs ที่ COMPLETED ต้องมี job_payments
-- ============================================================
SELECT 'COMPLETED jobs missing payment', COUNT(*)
FROM jobs j
LEFT JOIN job_payments jp ON j.job_id = jp.job_id
WHERE j.job_status = 'COMPLETED' AND jp.payment_id IS NULL

UNION ALL

-- ============================================================
-- 36. jobs ที่ SELECTED/IN_PROGRESS/COMPLETED ต้องมี selected_fl_id
-- ============================================================
SELECT 'SELECTED/IN_PROGRESS/COMPLETED jobs missing selected_fl_id', COUNT(*)
FROM jobs
WHERE job_status IN ('SELECTED','IN_PROGRESS','COMPLETED')
AND selected_fl_id IS NULL

UNION ALL

-- ============================================================
-- 37. fl_verification ต้องมีครบทุก freelancer
-- ============================================================
SELECT 'freelancers missing fl_verification', COUNT(*)
FROM freelancers f
LEFT JOIN fl_verification fv ON f.fl_id = fv.fl_id AND fv.is_latest = TRUE
WHERE fv.fl_verify_id IS NULL

UNION ALL

-- ============================================================
-- 38. em_verification ต้องมีครบทุก employer
-- ============================================================
SELECT 'employers missing em_verification', COUNT(*)
FROM employers e
LEFT JOIN em_verification ev ON e.em_id = ev.em_id AND ev.is_latest = TRUE
WHERE ev.em_verify_id IS NULL

UNION ALL

-- ============================================================
-- 39. freelancer ที่ VERIFIED ต้อง fl_verify_status ตรงกัน
-- ============================================================
SELECT 'fl_verify_status mismatch', COUNT(*)
FROM freelancers f
JOIN fl_verification fv ON f.fl_id = fv.fl_id AND fv.is_latest = TRUE
WHERE f.fl_verify_status != fv.fl_verify_status

UNION ALL

-- ============================================================
-- 40. employer ที่ VERIFIED ต้อง em_verify_status ตรงกัน
-- ============================================================
SELECT 'em_verify_status mismatch', COUNT(*)
FROM employers e
JOIN em_verification ev ON e.em_id = ev.em_id AND ev.is_latest = TRUE
WHERE e.em_verify_status != ev.em_verify_status;
