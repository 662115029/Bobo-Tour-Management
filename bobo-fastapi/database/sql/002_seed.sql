INSERT INTO admins (admin_id, name, password_hash, status, created_at) VALUES
('ad_001', 'James Carter',    '$2b$12$KIXe1Voss9WRSL1znk3I8eRBEBB8gFz3Nkq7v1sFQWqN2vT0kO5Y2', 'active',   '2025-01-05 08:00:00'),
('ad_002', 'Sarah Mitchell',  '$2b$12$LMNpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlM', 'active',   '2025-01-10 09:15:00'),
('ad_003', 'David Thompson',  '$2b$12$NoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmN', 'active',   '2025-02-01 10:00:00'),
('ad_004', 'Emily Watson',    '$2b$12$PqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoP', 'inactive', '2025-02-14 11:30:00'),
('ad_005', 'Michael Reed',    '$2b$12$RsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqR', 'active',   '2025-03-03 14:00:00');

INSERT INTO employers (em_id, em_username, em_password_hash, em_name, em_phone, em_address, em_bio, em_profile_image_url, em_verify_status, em_is_active, em_rating_avg, em_created_at, em_updated_at) VALUES
('em_001', 'techbkk_solutions', '$2b$12$AaBbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01', 'TechBKK Solutions Co., Ltd.', '0812345678', '128 Sukhumvit Rd, Khlong Toei, Bangkok 10110', 'We are a Bangkok-based software development company specializing in enterprise applications and cloud solutions.', 'https://example.com/profiles/em_001.jpg', 'VERIFIED', true, 4.7, '2025-01-15 09:00:00', '2026-03-10 14:22:00'),
('em_002', 'chiangmai_creative', '$2b$12$BbCcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0102', 'Chiang Mai Creative Studio', '0823456789', '55 Nimman Rd, Suthep, Mueang Chiang Mai 50200', 'A creative agency offering branding, graphic design, and digital marketing services in northern Thailand.', 'https://example.com/profiles/em_002.jpg', 'VERIFIED', true, 4.5, '2025-02-01 10:30:00', '2026-02-28 11:00:00'),
('em_003', 'phuket_hospitality', '$2b$12$CcDdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz010203', 'Phuket Hospitality Group', '0834567890', '77 Thalang Rd, Muang, Phuket 83000', 'Hospitality management company operating boutique hotels and resorts across Phuket island.', 'https://example.com/profiles/em_003.jpg', 'VERIFIED', true, 4.2, '2025-02-10 08:45:00', '2026-01-20 09:30:00'),
('em_004', 'northgate_logistics', '$2b$12$DdEeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01020304', 'Northgate Logistics Ltd.', '0845678901', '200 Superhighway Rd, Mueang, Chiang Rai 57000', 'Logistics and supply chain company serving Northern Thailand with warehousing and freight solutions.', 'https://example.com/profiles/em_004.jpg', 'PENDING', true, 3.8, '2025-03-05 13:00:00', '2026-03-05 13:00:00'),
('em_005', 'siam_fintech', '$2b$12$EeFfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0102030405', 'Siam FinTech Corp', '0856789012', '300 Silom Rd, Bang Rak, Bangkok 10500', 'Fintech startup providing digital payment and lending solutions across Southeast Asia.', 'https://example.com/profiles/em_005.jpg', 'VERIFIED', true, 4.9, '2025-01-20 11:00:00', '2026-04-01 10:00:00'),
('em_006', 'korat_builders', '$2b$12$FfGgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz010203040506', 'Korat Builders & Contractors', '0867890123', '14 Mittraphap Rd, Mueang, Nakhon Ratchasima 30000', 'Construction and property development firm handling residential and commercial projects in Isan.', 'https://example.com/profiles/em_006.jpg', 'NOT_VERIFIED', false, 3.2, '2025-04-12 14:30:00', '2025-10-01 09:00:00'),
('em_007', 'bkk_media_house', '$2b$12$GgHhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01020304050607', 'Bangkok Media House Co., Ltd.', '0878901234', '89 Ratchadaphisek Rd, Din Daeng, Bangkok 10400', 'Full-service media production company specializing in TV commercials, video content, and photography.', 'https://example.com/profiles/em_007.jpg', 'VERIFIED', true, 4.6, '2025-02-22 09:00:00', '2026-03-15 16:45:00'),
('em_008', 'samui_realestate', '$2b$12$HhIiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0102030405060708', 'Koh Samui Real Estate Partners', '0889012345', '33 Chaweng Beach Rd, Ko Samui, Surat Thani 84320', 'Property consultancy managing villa rentals, sales, and investment opportunities on Koh Samui.', 'https://example.com/profiles/em_008.jpg', 'VERIFIED', true, 4.3, '2025-03-18 10:15:00', '2026-02-10 12:00:00'),
('em_009', 'ayutthaya_tours', '$2b$12$IiJjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz010203040506070809', 'Ayutthaya Heritage Tours', '0890123456', '10 U Thong Rd, Phra Nakhon Si Ayutthaya 13000', 'Tour operator offering historical and cultural excursions around Ayutthaya and Central Thailand.', 'https://example.com/profiles/em_009.jpg', 'PENDING', true, 4.0, '2025-04-01 08:00:00', '2026-01-05 10:30:00'),
('em_010', 'lampang_woodcraft', '$2b$12$JjKkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz01020304050607080910', 'Lampang Woodcraft Enterprise', '0801234567', '60 Takrao Noi Rd, Mueang, Lampang 52000', 'Traditional woodcraft and furniture manufacturer exporting handmade products internationally.', 'https://example.com/profiles/em_010.jpg', 'NOT_VERIFIED', true, 3.5, '2025-05-07 11:00:00', '2025-11-20 09:00:00'),
('em_011', 'pattaya_events', '$2b$12$KkLlMmNnOoPpQqRrSsTtUuVvWwXxYyZz0102030405060708091011', 'Pattaya Events & Entertainment', '0811223344', '22 Second Rd, Bang Lamung, Chonburi 20150', 'Event management company organizing concerts, corporate events, and exhibitions in the Eastern Seaboard.', 'https://example.com/profiles/em_011.jpg', 'VERIFIED', true, 4.4, '2025-03-25 14:00:00', '2026-04-05 15:30:00'),
('em_012', 'hatyai_export', '$2b$12$LlMmNnOoPpQqRrSsTtUuVvWwXxYyZz010203040506070809101112', 'Hat Yai Export Trading Co.', '0822334455', '150 Niphat Uthit 3 Rd, Hat Yai, Songkhla 90110', 'Export trading company dealing in agricultural products, rubber, and consumer goods to ASEAN markets.', 'https://example.com/profiles/em_012.jpg', 'VERIFIED', true, 4.1, '2025-02-15 09:30:00', '2026-03-22 11:00:00'),
('em_013', 'chiangrai_agro', '$2b$12$MmNnOoPpQqRrSsTtUuVvWwXxYyZz01020304050607080910111213', 'Chiang Rai AgroTech Co., Ltd.', '0833445566', '99 Phahonyothin Rd, Mueang, Chiang Rai 57000', 'Agricultural technology company providing smart farming solutions and organic produce distribution.', 'https://example.com/profiles/em_013.jpg', 'PENDING', true, 3.9, '2025-06-01 10:00:00', '2026-02-14 08:45:00'),
('em_014', 'bkk_healthclinic', '$2b$12$NnOoPpQqRrSsTtUuVvWwXxYyZz0102030405060708091011121314', 'Bangkok Health Clinic Network', '0844556677', '500 Phetchaburi Rd, Ratchathewi, Bangkok 10400', 'Private healthcare network with multiple clinics across Bangkok offering outpatient and specialist services.', 'https://example.com/profiles/em_014.jpg', 'VERIFIED', true, 4.8, '2025-01-28 07:30:00', '2026-03-30 13:00:00'),
('em_015', 'krabi_ecotravel', '$2b$12$OoPpQqRrSsTtUuVvWwXxYyZz010203040506070809101112131415', 'Krabi Eco Travel Agency', '0855667788', '18 Maharaj Rd, Mueang, Krabi 81000', 'Eco-tourism agency offering sustainable island hopping, kayaking, and snorkeling tours around Krabi.', 'https://example.com/profiles/em_015.jpg', 'VERIFIED', true, 4.6, '2025-04-20 11:30:00', '2026-04-10 10:00:00'),
('em_016', 'udon_foodbiz', '$2b$12$PpQqRrSsTtUuVvWwXxYyZz01020304050607080910111213141516', 'Udon Thani Food Business Group', '0866778899', '45 Pho Si Rd, Mueang, Udon Thani 41000', 'Food and beverage company operating restaurant chains and catering services in Northeastern Thailand.', 'https://example.com/profiles/em_016.jpg', 'NOT_VERIFIED', false, 2.9, '2025-07-10 12:00:00', '2025-09-01 10:00:00'),
('em_017', 'pathumwan_retail', '$2b$12$QqRrSsTtUuVvWwXxYyZz0102030405060708091011121314151617', 'Pathumwan Retail Solutions', '0877889900', '101 Rama I Rd, Pathumwan, Bangkok 10330', 'Retail consultancy and store management company operating fashion and lifestyle shops in Bangkok malls.', 'https://example.com/profiles/em_017.jpg', 'VERIFIED', true, 4.3, '2025-02-08 13:00:00', '2026-03-18 16:00:00'),
('em_018', 'phuket_webagency', '$2b$12$RrSsTtUuVvWwXxYyZz010203040506070809101112131415161718', 'Phuket Web Agency', '0888990011', '30 Yaowarat Rd, Mueang, Phuket 83000', 'Web design and digital marketing agency serving tourism and hospitality businesses in Phuket.', 'https://example.com/profiles/em_018.jpg', 'PENDING', true, 4.0, '2025-05-15 09:00:00', '2026-01-30 14:00:00'),
('em_019', 'chonburi_manufact', '$2b$12$SsTtUuVvWwXxYyZz01020304050607080910111213141516171819', 'Chonburi Manufacturing Corp', '0899001122', '250 Sukhumvit Rd, Mueang, Chonburi 20000', 'Industrial manufacturing company producing auto parts and electronic components for export.', 'https://example.com/profiles/em_019.jpg', 'VERIFIED', true, 4.2, '2025-03-30 08:00:00', '2026-04-12 09:30:00'),
('em_020', 'loei_adventure', '$2b$12$TtUuVvWwXxYyZz0102030405060708091011121314151617181920', 'Loei Adventure Co., Ltd.', '0800112233', '5 Chumsai Rd, Mueang, Loei 42000', 'Outdoor adventure company offering trekking, camping, and zip-line experiences in Loei Province.', 'https://example.com/profiles/em_020.jpg', 'NOT_VERIFIED', false, 3.4, '2025-08-01 10:00:00', '2025-10-15 11:00:00');

INSERT INTO freelancers (fl_id, line_user_id, fl_name, fl_pin_hash, fl_date_of_birth, fl_address, fl_bio, fl_profile_image_url, fl_verify_status, fl_is_active, fl_rating_avg, fl_created_at, fl_updated_at) VALUES
('fl_001', 'Uab3f1c2e4d5e6f7a8b', 'Oliver Bennett', '$2b$12$AbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYz01', '1992-04-15', '22 Nimmanhaemin Rd, Suthep, Mueang Chiang Mai 50200', 'Full-stack web developer with 7 years of experience in React, Node.js, and cloud infrastructure.', 'https://example.com/profiles/fl_001.jpg', 'VERIFIED', true, 4.8, '2025-01-20 10:00:00', '2026-03-12 14:00:00'),
('fl_002', 'Ubc4d2e3f5a6b7c8d9', 'Sophia Johnson', '$2b$12$BcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZa02', '1995-07-22', '88 Sukhumvit Rd, Khlong Toei, Bangkok 10110', 'Freelance graphic designer and illustrator specializing in brand identity and packaging design.', 'https://example.com/profiles/fl_002.jpg', 'VERIFIED', true, 4.6, '2025-01-25 11:00:00', '2026-02-20 09:00:00'),
('fl_003', 'Ucd5e3f4a6b7c8d9e0', 'Nathan Clarke', '$2b$12$CdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAb03', '1990-11-08', '45 Thalang Rd, Mueang, Phuket 83000', 'Digital marketing specialist with expertise in SEO, Google Ads, and social media strategy.', 'https://example.com/profiles/fl_003.jpg', 'VERIFIED', true, 4.3, '2025-02-01 09:00:00', '2026-03-01 11:00:00'),
('fl_004', 'Ude6f4a5b7c8d9e0f1', 'Emma Richardson', '$2b$12$DeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBc04', '1997-03-30', '12 Phahonyothin Rd, Mueang, Chiang Rai 57000', 'Content writer and copywriter with a background in travel, hospitality, and lifestyle industries.', 'https://example.com/profiles/fl_004.jpg', 'PENDING', true, 4.1, '2025-02-10 13:30:00', '2026-01-15 10:00:00'),
('fl_005', 'Uef7a5b6c8d9e0f1a2', 'Liam Foster', '$2b$12$EfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCd05', '1993-09-14', '300 Sukhumvit Rd, Bang Na, Bangkok 10260', 'Mobile app developer (iOS & Android) with 5 years of experience building fintech and e-commerce apps.', 'https://example.com/profiles/fl_005.jpg', 'VERIFIED', true, 4.9, '2025-02-15 08:00:00', '2026-04-01 12:00:00'),
('fl_006', 'Uf08b6c7d9e0f1a2b3', 'Isabella Moore', '$2b$12$FgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDe06', '1996-01-19', '60 Mittraphap Rd, Mueang, Nakhon Ratchasima 30000', 'UI/UX designer focused on user research, wireframing, and prototyping for web and mobile platforms.', 'https://example.com/profiles/fl_006.jpg', 'VERIFIED', true, 4.5, '2025-03-01 10:00:00', '2026-03-20 15:00:00'),
('fl_007', 'Ua19c7d8e0f1a2b3c4', 'James Harper', '$2b$12$GhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEf07', '1988-06-25', '18 Yaowarat Rd, Mueang, Phuket 83000', 'Photographer and videographer specializing in commercial, real estate, and event photography.', 'https://example.com/profiles/fl_007.jpg', 'NOT_VERIFIED', false, 3.7, '2025-03-10 14:00:00', '2025-08-01 09:00:00'),
('fl_008', 'Ub20d8e9f1a2b3c4d5', 'Charlotte Evans', '$2b$12$HiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFg08', '1994-12-05', '77 Chaweng Beach Rd, Ko Samui, Surat Thani 84320', 'Freelance translator (English-Thai) and interpreter with experience in legal and medical documents.', 'https://example.com/profiles/fl_008.jpg', 'VERIFIED', true, 4.7, '2025-03-15 09:00:00', '2026-02-25 11:00:00'),
('fl_009', 'Uc31e9f0a2b3c4d5e6', 'William Turner', '$2b$12$IjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGh09', '1991-08-17', '100 Superhighway Rd, Mueang, Chiang Rai 57000', 'Data analyst and business intelligence consultant with expertise in Python, SQL, and Power BI.', 'https://example.com/profiles/fl_009.jpg', 'VERIFIED', true, 4.4, '2025-04-01 10:00:00', '2026-03-10 13:00:00'),
('fl_010', 'Ud42f0a1b3c4d5e6f7', 'Mia Anderson', '$2b$12$JkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHi10', '1998-02-28', '50 Nimman Rd, Suthep, Mueang Chiang Mai 50200', 'Social media manager and content creator managing Instagram and TikTok for lifestyle and food brands.', 'https://example.com/profiles/fl_010.jpg', 'PENDING', true, 3.9, '2025-04-10 11:00:00', '2026-01-22 10:00:00'),
('fl_011', 'Ue53a1b2c4d5e6f7a8', 'Henry Walker', '$2b$12$KlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIj11', '1987-05-10', '250 Silom Rd, Bang Rak, Bangkok 10500', 'Senior software engineer specializing in backend systems, microservices, and DevOps automation.', 'https://example.com/profiles/fl_011.jpg', 'VERIFIED', true, 4.9, '2025-01-10 08:00:00', '2026-04-10 09:00:00'),
('fl_012', 'Uf64b2c3d5e6f7a8b9', 'Amelia Scott', '$2b$12$LmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJk12', '1999-10-03', '30 Hat Yai-Sadao Rd, Hat Yai, Songkhla 90110', 'Freelance accountant and bookkeeper with knowledge of Thai tax law and QuickBooks.', 'https://example.com/profiles/fl_012.jpg', 'VERIFIED', true, 4.3, '2025-04-20 09:30:00', '2026-02-18 10:00:00'),
('fl_013', 'Ua75c3d4e6f7a8b9c0', 'Lucas Green', '$2b$12$MnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKl13', '1993-03-22', '90 Pho Si Rd, Mueang, Udon Thani 41000', 'E-commerce specialist helping SMEs set up and scale Shopify and Lazada stores across Thailand.', 'https://example.com/profiles/fl_013.jpg', 'NOT_VERIFIED', true, 3.5, '2025-05-01 13:00:00', '2025-11-10 09:00:00'),
('fl_014', 'Ub86d4e5f7a8b9c0d1', 'Grace Hall', '$2b$12$NoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLm14', '1996-07-14', '40 Chaweng Noi Rd, Ko Samui, Surat Thani 84320', 'Yoga and wellness coach offering personal training and corporate wellness programs.', 'https://example.com/profiles/fl_014.jpg', 'VERIFIED', true, 4.8, '2025-05-10 08:00:00', '2026-03-28 14:00:00'),
('fl_015', 'Uc97e5f6a8b9c0d1e2', 'Benjamin Adams', '$2b$12$OpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMn15', '1990-12-01', '70 Ratchadaphisek Rd, Din Daeng, Bangkok 10400', 'Video editor and motion graphics designer for YouTube channels, ads, and corporate presentations.', 'https://example.com/profiles/fl_015.jpg', 'PENDING', false, 3.6, '2025-05-20 12:00:00', '2025-12-01 10:00:00'),
('fl_016', 'Ud08f6a7b9c0d1e2f3', 'Ella Baker', '$2b$12$PqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNo16', '1995-04-28', '15 Maharaj Rd, Mueang, Krabi 81000', 'Marine biologist turned dive instructor and underwater photographer based in Krabi.', 'https://example.com/profiles/fl_016.jpg', 'VERIFIED', true, 4.6, '2025-06-01 09:00:00', '2026-03-15 11:00:00'),
('fl_017', 'Ue19a7b8c0d1e2f3a4', 'Daniel White', '$2b$12$QrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOp17', '1989-09-09', '200 Second Rd, Bang Lamung, Pattaya, Chonburi 20150', 'IT infrastructure consultant managing network setups and cybersecurity audits for hotels and businesses.', 'https://example.com/profiles/fl_017.jpg', 'VERIFIED', true, 4.2, '2025-06-10 11:00:00', '2026-02-22 09:00:00'),
('fl_018', 'Uf20b8c9d1e2f3a4b5', 'Chloe Martin', '$2b$12$RsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPq18', '1997-01-31', '80 Takrao Noi Rd, Mueang, Lampang 52000', 'Freelance interior designer specializing in Lanna-inspired and contemporary residential interiors.', 'https://example.com/profiles/fl_018.jpg', 'NOT_VERIFIED', false, 3.3, '2025-06-20 14:00:00', '2025-09-15 09:00:00'),
('fl_019', 'Ua31c9d0e2f3a4b5c6', 'Alexander Thompson', '$2b$12$StUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQr19', '1992-06-18', '120 Phetchaburi Rd, Ratchathewi, Bangkok 10400', 'Financial advisor and investment consultant with expertise in Thai equities and mutual funds.', 'https://example.com/profiles/fl_019.jpg', 'VERIFIED', true, 4.7, '2025-07-01 08:30:00', '2026-04-05 13:00:00'),
('fl_020', 'Ub42d0e1f3a4b5c6d7', 'Zoe Mitchell', '$2b$12$TuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRs20', '1999-11-25', '35 Chumsai Rd, Mueang, Loei 42000', 'Eco-tourism guide and travel blogger covering trekking routes in Loei and Northern Thailand.', 'https://example.com/profiles/fl_020.jpg', 'PENDING', true, 4.0, '2025-07-10 10:00:00', '2026-01-30 11:00:00'),
('fl_021', 'Uc53e1f2a4b5c6d7e8', 'Ryan Davis', '$2b$12$UvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrSt21', '1991-02-14', '55 Nakhon In Rd, Mueang, Nonthaburi 11000', 'Front-end developer specializing in Vue.js and Nuxt.js with a focus on performance and accessibility.', 'https://example.com/profiles/fl_021.jpg', 'VERIFIED', true, 4.5, '2025-07-15 09:00:00', '2026-03-25 14:00:00'),
('fl_022', 'Ud64f2a3b5c6d7e8f9', 'Hannah Lewis', '$2b$12$VwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTu22', '1994-08-07', '10 U Thong Rd, Phra Nakhon Si Ayutthaya 13000', 'Museum curator and cultural heritage consultant providing content for tourism and education projects.', 'https://example.com/profiles/fl_022.jpg', 'VERIFIED', true, 4.4, '2025-07-20 11:00:00', '2026-02-14 10:00:00'),
('fl_023', 'Ue75a3b4c6d7e8f9a0', 'Jack Robinson', '$2b$12$WxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUv23', '1988-10-30', '180 Phahonyothin Rd, Chatuchak, Bangkok 10900', 'DevOps engineer with expertise in AWS, Docker, Kubernetes, and CI/CD pipeline management.', 'https://example.com/profiles/fl_023.jpg', 'VERIFIED', true, 4.8, '2025-08-01 08:00:00', '2026-04-08 09:30:00'),
('fl_024', 'Uf86b4c5d7e8f9a0b1', 'Victoria King', '$2b$12$XyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVw24', '1996-05-05', '25 Thalang Rd, Mueang, Phuket 83000', 'HR consultant and recruitment specialist helping international companies hire local Thai talent.', 'https://example.com/profiles/fl_024.jpg', 'PENDING', true, 3.8, '2025-08-10 13:00:00', '2026-01-10 10:00:00'),
('fl_025', 'Ua97c5d6e8f9a0b1c2', 'Samuel Wright', '$2b$12$YzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWx25', '1993-01-12', '60 Nimman Rd, Suthep, Mueang Chiang Mai 50200', 'Music producer and audio engineer working with local artists and advertising agencies in Chiang Mai.', 'https://example.com/profiles/fl_025.jpg', 'NOT_VERIFIED', true, 3.6, '2025-08-15 10:30:00', '2025-12-20 09:00:00'),
('fl_026', 'Ub08d6e7f9a0b1c2d3', 'Lily Harris', '$2b$12$ZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXy26', '1998-07-19', '90 Niphat Uthit 1 Rd, Hat Yai, Songkhla 90110', 'Fashion designer and tailor producing custom garments and alterations for clients in Southern Thailand.', 'https://example.com/profiles/fl_026.jpg', 'VERIFIED', true, 4.3, '2025-08-20 09:00:00', '2026-03-05 12:00:00'),
('fl_027', 'Uc19e7f8a0b1c2d3e4', 'Thomas Brown', '$2b$12$AbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYz27', '1990-03-26', '35 Mittraphap Rd, Mueang, Khon Kaen 40000', 'Civil engineer and project manager with experience in road construction and public infrastructure projects.', 'https://example.com/profiles/fl_027.jpg', 'VERIFIED', true, 4.6, '2025-09-01 08:30:00', '2026-03-18 10:00:00'),
('fl_028', 'Ud20f8a9b1c2d3e4f5', 'Sophie Taylor', '$2b$12$BcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZa28', '1995-10-11', '70 Sukhumvit Rd, Mueang, Chonburi 20000', 'Legal consultant specializing in Thai business law, contract drafting, and corporate registration.', 'https://example.com/profiles/fl_028.jpg', 'VERIFIED', true, 4.9, '2025-09-05 11:00:00', '2026-04-12 14:00:00'),
('fl_029', 'Ue31a9b0c2d3e4f5a6', 'George Jackson', '$2b$12$CdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAb29', '1986-12-22', '110 Rama I Rd, Pathumwan, Bangkok 10330', 'Executive chef offering private dining, cooking classes, and menu consultation for restaurants.', 'https://example.com/profiles/fl_029.jpg', 'NOT_VERIFIED', false, 3.4, '2025-09-10 14:00:00', '2025-11-30 10:00:00'),
('fl_030', 'Uf42b0c1d3e4f5a6b7', 'Nora Martinez', '$2b$12$DeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBc30', '1997-05-16', '20 Chumsai Rd, Mueang, Loei 42000', 'Environmental consultant conducting EIA studies and sustainability reports for development projects.', 'https://example.com/profiles/fl_030.jpg', 'PENDING', true, 4.0, '2025-09-15 09:30:00', '2026-02-05 11:00:00'),
('fl_031', 'Ua53c1d2e4f5a6b7c8', 'Joshua Wilson', '$2b$12$EfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCd31', '1992-08-04', '150 Pho Si Rd, Mueang, Udon Thani 41000', 'Agricultural engineer advising on irrigation systems and crop optimization for farms in Isan.', 'https://example.com/profiles/fl_031.jpg', 'VERIFIED', true, 4.2, '2025-09-20 10:00:00', '2026-03-22 13:00:00'),
('fl_032', 'Ub64d2e3f5a6b7c8d9', 'Penelope Collins', '$2b$12$FgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDe32', '1999-02-09', '40 Nimmanhaemin Rd, Suthep, Mueang Chiang Mai 50200', 'Online English tutor and curriculum developer with CELTA certification and 4 years of experience.', 'https://example.com/profiles/fl_032.jpg', 'VERIFIED', true, 4.7, '2025-10-01 08:00:00', '2026-04-01 10:00:00'),
('fl_033', 'Uc75e3f4a6b7c8d9e0', 'Ethan Nelson', '$2b$12$GhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEf33', '1991-11-27', '60 Second Rd, Bang Lamung, Pattaya, Chonburi 20150', 'Blockchain developer building smart contracts and DeFi applications on Ethereum and Solana.', 'https://example.com/profiles/fl_033.jpg', 'PENDING', true, 4.1, '2025-10-08 11:00:00', '2026-01-28 12:00:00'),
('fl_034', 'Ud86f4a5b7c8d9e0f1', 'Aria Rodriguez', '$2b$12$HiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFg34', '1994-04-21', '5 Phahonyothin Rd, Mueang, Chiang Rai 57000', 'Landscape architect designing garden spaces, green rooftops, and resort grounds across Thailand.', 'https://example.com/profiles/fl_034.jpg', 'VERIFIED', true, 4.5, '2025-10-15 09:00:00', '2026-03-30 15:00:00'),
('fl_035', 'Ue97a5b6c8d9e0f1a2', 'Luke Phillips', '$2b$12$IjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGh35', '1989-07-13', '80 Yaowarat Rd, Mueang, Phuket 83000', 'Marine mechanic and boat maintenance specialist servicing yachts and speedboats in Phuket.', 'https://example.com/profiles/fl_035.jpg', 'NOT_VERIFIED', false, 3.1, '2025-10-20 14:00:00', '2025-12-10 10:00:00'),
('fl_036', 'Uf08b6c7d9e0f1a2b3c', 'Scarlett Campbell', '$2b$12$JkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHi36', '1996-09-02', '200 Maharaj Rd, Mueang, Krabi 81000', 'Wedding planner and event coordinator managing destination weddings in Krabi and Koh Lanta.', 'https://example.com/profiles/fl_036.jpg', 'VERIFIED', true, 4.8, '2025-11-01 09:00:00', '2026-04-08 11:00:00'),
('fl_037', 'Ua19c7d8e0f1a2b3c4d', 'Aaron Parker', '$2b$12$KlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIj37', '1993-12-17', '100 Ratchadaphisek Rd, Huai Khwang, Bangkok 10310', 'Cybersecurity analyst conducting penetration testing and vulnerability assessments for companies.', 'https://example.com/profiles/fl_037.jpg', 'VERIFIED', true, 4.6, '2025-11-05 10:00:00', '2026-03-12 13:00:00'),
('fl_038', 'Ub20d8e9f1a2b3c4d5e', 'Maya Evans', '$2b$12$LmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJk38', '1998-03-06', '30 Takrao Noi Rd, Mueang, Lampang 52000', 'Textile artist and craft workshop facilitator teaching traditional Northern Thai weaving techniques.', 'https://example.com/profiles/fl_038.jpg', 'PENDING', true, 3.9, '2025-11-10 11:00:00', '2026-02-02 10:00:00'),
('fl_039', 'Uc31e9f0a2b3c4d5e6f', 'Dylan Stewart', '$2b$12$MnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKl39', '1990-06-23', '50 Hat Yai-Sadao Rd, Hat Yai, Songkhla 90110', 'Supply chain consultant optimizing procurement and inventory processes for retail and manufacturing clients.', 'https://example.com/profiles/fl_039.jpg', 'VERIFIED', true, 4.3, '2025-11-15 08:30:00', '2026-04-05 14:00:00'),
('fl_040', 'Ud42f0a1b3c4d5e6f7a', 'Aurora Hughes', '$2b$12$NoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLm40', '1995-01-08', '75 Nakhon In Rd, Mueang, Nonthaburi 11000', 'Child psychologist offering school counseling and family therapy services in the Bangkok area.', 'https://example.com/profiles/fl_040.jpg', 'VERIFIED', true, 4.9, '2025-11-20 09:00:00', '2026-04-10 10:00:00'),
('fl_041', 'Ue53a1b2c4d5e6f7a8b', 'Felix Sanchez', '$2b$12$OpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMn41', '1987-10-19', '90 Chaweng Beach Rd, Ko Samui, Surat Thani 84320', 'Boat charter operator and sailing instructor offering day trips and overnight cruises around Samui.', 'https://example.com/profiles/fl_041.jpg', 'NOT_VERIFIED', true, 3.7, '2025-12-01 10:00:00', '2026-01-05 09:00:00'),
('fl_042', 'Uf64b2c3d5e6f7a8b9c', 'Iris Long', '$2b$12$PqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNo42', '1997-08-14', '55 U Thong Rd, Phra Nakhon Si Ayutthaya 13000', 'Archaeologist and heritage tour guide leading educational tours of Ayutthaya historical sites.', 'https://example.com/profiles/fl_042.jpg', 'VERIFIED', true, 4.4, '2025-12-05 11:00:00', '2026-03-28 12:00:00'),
('fl_043', 'Ua75c3d4e6f7a8b9c0d', 'Owen Foster', '$2b$12$QrStUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOp43', '1992-04-02', '110 Phetchaburi Rd, Mueang, Phetchaburi 76000', 'Drone operator and aerial photographer holding a certified CAPT license for commercial drone use.', 'https://example.com/profiles/fl_043.jpg', 'PENDING', false, 3.5, '2025-12-10 14:00:00', '2026-01-20 09:00:00'),
('fl_044', 'Ub86d4e5f7a8b9c0d1e', 'Ruby Price', '$2b$12$RsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPq44', '1999-06-30', '20 Mittraphap Rd, Mueang, Khon Kaen 40000', 'Nutritionist and meal prep consultant offering personalized diet plans for athletes and busy professionals.', 'https://example.com/profiles/fl_044.jpg', 'VERIFIED', true, 4.6, '2025-12-15 09:00:00', '2026-04-02 11:00:00'),
('fl_045', 'Uc97e5f6a8b9c0d1e2f', 'Isaac Bell', '$2b$12$StUvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQr45', '1991-02-20', '65 Superhighway Rd, Mueang, Chiang Rai 57000', 'Machine learning engineer building NLP and computer vision models for Thai-language applications.', 'https://example.com/profiles/fl_045.jpg', 'VERIFIED', true, 4.8, '2025-12-20 08:00:00', '2026-04-14 13:00:00'),
('fl_046', 'Ud08f6a7b9c0d1e2f3a', 'Pearl Morgan', '$2b$12$TuVwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRs46', '1996-11-11', '40 Second Rd, Bang Lamung, Pattaya, Chonburi 20150', 'Spa therapist and wellness consultant with certifications in Thai massage and aromatherapy.', 'https://example.com/profiles/fl_046.jpg', 'VERIFIED', true, 4.5, '2026-01-05 10:00:00', '2026-04-03 15:00:00'),
('fl_047', 'Ue19a7b8c0d1e2f3a4b', 'Spencer Ross', '$2b$12$UvWxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrSt47', '1989-07-07', '80 Silom Rd, Bang Rak, Bangkok 10500', 'Corporate trainer and keynote speaker delivering leadership and communication workshops.', 'https://example.com/profiles/fl_047.jpg', 'NOT_VERIFIED', false, 3.2, '2026-01-10 11:00:00', '2026-02-28 09:00:00'),
('fl_048', 'Uf20b8c9d1e2f3a4b5c', 'Violet Reed', '$2b$12$VwXyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTu48', '1994-09-25', '15 Yaowarat Rd, Mueang, Phuket 83000', 'Jewellery designer crafting custom pieces using local gemstones and silver for boutiques in Phuket.', 'https://example.com/profiles/fl_048.jpg', 'VERIFIED', true, 4.3, '2026-01-15 09:00:00', '2026-04-06 12:00:00'),
('fl_049', 'Ua31c9d0e2f3a4b5c6d', 'Maxwell Cooper', '$2b$12$WxYzAbCdEfGhIjKlMnOpQrStUvWxYzAbCdEfGhIjKlMnOpQrStUv49', '1993-03-13', '30 Phahonyothin Rd, Mueang, Chiang Rai 57000', 'Solar energy consultant helping homeowners and businesses install and manage solar panel systems.', 'https://example.com/profiles/fl_049.jpg', 'PENDING', true, 4.0, '2026-01-20 10:30:00', '2026-04-10 11:00:00'),
('fl_050', 'Ub42d0e1f3a4b5c6d7e', 'Daisy Ward', '$2b$12$XyZaBcDeFgHiJkLmNoPqRsTuVwXyZaBcDeFgHiJkLmNoPqRsTuVw50', '1998-12-04', '50 Nimman Rd, Suthep, Mueang Chiang Mai 50200', 'Podcast producer and audio content creator managing branded podcasts for tech and lifestyle companies.', 'https://example.com/profiles/fl_050.jpg', 'VERIFIED', true, 4.7, '2026-02-01 09:00:00', '2026-04-15 14:00:00');

INSERT INTO fl_vehicle (fl_vehicle_id, fl_id, fl_vehicle_type, fl_vehicle_brand, fl_vehicle_model, fl_vehicle_year, fl_vehicle_seat_capa, fl_vehicle_license_plate) VALUES
('fv_001', 'fl_001', 'VAN', 'Toyota', 'Commuter', 2021, 12, 'Chiang Mai 1001'),
('fv_002', 'fl_001', 'VAN', 'Toyota', 'Commuter', 2022, 12, 'Chiang Mai 1002'),
('fv_003', 'fl_002', 'VAN', 'Hyundai', 'H1', 2020, 10, 'Bangkok 2001'),
('fv_004', 'fl_003', 'VAN', 'Toyota', 'Commuter', 2022, 12, 'Phuket 3001'),
('fv_005', 'fl_004', 'VAN', 'Hyundai', 'H1', 2021, 10, 'Chiang Rai 4001'),
('fv_006', 'fl_005', 'VAN', 'Hyundai', 'H1', 2023, 10, 'Bangkok 2002'),
('fv_007', 'fl_006', 'VAN', 'Toyota', 'Commuter', 2020, 12, 'Nakhon Ratchasima 6001'),
('fv_008', 'fl_007', 'VAN', 'Hyundai', 'H1', 2021, 10, 'Phuket 3002'),
('fv_009', 'fl_007', 'VAN', 'Toyota', 'Commuter', 2019, 12, 'Phuket 3003'),
('fv_010', 'fl_008', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Surat Thani 8001'),
('fv_011', 'fl_009', 'VAN', 'Toyota', 'Commuter', 2021, 12, 'Chiang Rai 4002'),
('fv_012', 'fl_010', 'VAN', 'Toyota', 'Commuter', 2020, 12, 'Chiang Mai 1003'),
('fv_013', 'fl_011', 'VAN', 'Toyota', 'Commuter', 2023, 12, 'Bangkok 2003'),
('fv_014', 'fl_011', 'VAN', 'Toyota', 'Commuter', 2022, 12, 'Bangkok 2004'),
('fv_015', 'fl_012', 'VAN', 'Hyundai', 'H1', 2021, 10, 'Songkhla 12001'),
('fv_016', 'fl_013', 'VAN', 'Hyundai', 'H1', 2020, 10, 'Udon Thani 13001'),
('fv_017', 'fl_014', 'VAN', 'Toyota', 'Commuter', 2022, 12, 'Surat Thani 14001'),
('fv_018', 'fl_015', 'VAN', 'Toyota', 'Commuter', 2021, 12, 'Bangkok 2005'),
('fv_019', 'fl_016', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Krabi 16001'),
('fv_020', 'fl_017', 'VAN', 'Toyota', 'Commuter', 2020, 12, 'Chonburi 17001'),
('fv_021', 'fl_017', 'VAN', 'Toyota', 'Commuter', 2021, 12, 'Chonburi 17002'),
('fv_022', 'fl_018', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Lampang 18001'),
('fv_023', 'fl_019', 'VAN', 'Hyundai', 'H1', 2023, 10, 'Bangkok 2006'),
('fv_024', 'fl_020', 'VAN', 'Hyundai', 'H1', 2021, 10, 'Loei 20001'),
('fv_025', 'fl_021', 'VAN', 'Toyota', 'Commuter', 2022, 12, 'Nonthaburi 21001'),
('fv_026', 'fl_022', 'VAN', 'Toyota', 'Commuter', 2020, 12, 'Ayutthaya 22001'),
('fv_027', 'fl_023', 'VAN', 'Toyota', 'Commuter', 2023, 12, 'Bangkok 2007'),
('fv_028', 'fl_023', 'VAN', 'Toyota', 'Commuter', 2021, 12, 'Bangkok 2008'),
('fv_029', 'fl_024', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Phuket 3004'),
('fv_030', 'fl_025', 'VAN', 'Hyundai', 'H1', 2021, 10, 'Chiang Mai 1004'),
('fv_031', 'fl_026', 'VAN', 'Toyota', 'Commuter', 2020, 12, 'Songkhla 26001'),
('fv_032', 'fl_027', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Khon Kaen 27001'),
('fv_033', 'fl_028', 'VAN', 'Toyota', 'Commuter', 2023, 12, 'Chonburi 28001'),
('fv_034', 'fl_029', 'VAN', 'Toyota', 'Commuter', 2019, 12, 'Bangkok 2009'),
('fv_035', 'fl_030', 'VAN', 'Hyundai', 'H1', 2021, 10, 'Loei 30001'),
('fv_036', 'fl_031', 'VAN', 'Toyota', 'Commuter', 2022, 12, 'Udon Thani 31001'),
('fv_037', 'fl_032', 'VAN', 'Toyota', 'Commuter', 2021, 12, 'Chiang Mai 1005'),
('fv_038', 'fl_033', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Chonburi 33001'),
('fv_039', 'fl_034', 'VAN', 'Toyota', 'Commuter', 2022, 12, 'Chiang Rai 34001'),
('fv_040', 'fl_035', 'VAN', 'Toyota', 'Commuter', 2020, 12, 'Phuket 3005'),
('fv_041', 'fl_036', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Krabi 36001'),
('fv_042', 'fl_036', 'VAN', 'Toyota', 'Commuter', 2021, 12, 'Krabi 36002'),
('fv_043', 'fl_037', 'VAN', 'Toyota', 'Commuter', 2023, 12, 'Bangkok 2010'),
('fv_044', 'fl_038', 'VAN', 'Hyundai', 'H1', 2021, 10, 'Lampang 38001'),
('fv_045', 'fl_039', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Songkhla 39001'),
('fv_046', 'fl_040', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Nonthaburi 40001'),
('fv_047', 'fl_041', 'VAN', 'Toyota', 'Commuter', 2020, 12, 'Surat Thani 41001'),
('fv_048', 'fl_042', 'VAN', 'Toyota', 'Commuter', 2021, 12, 'Ayutthaya 42001'),
('fv_049', 'fl_043', 'VAN', 'Toyota', 'Commuter', 2022, 12, 'Phetchaburi 43001'),
('fv_050', 'fl_044', 'VAN', 'Hyundai', 'H1', 2021, 10, 'Khon Kaen 44001'),
('fv_051', 'fl_045', 'VAN', 'Toyota', 'Commuter', 2023, 12, 'Chiang Rai 45001'),
('fv_052', 'fl_046', 'VAN', 'Hyundai', 'H1', 2022, 10, 'Chonburi 46001'),
('fv_053', 'fl_047', 'VAN', 'Toyota', 'Commuter', 2020, 12, 'Bangkok 2011'),
('fv_054', 'fl_048', 'VAN', 'Toyota', 'Commuter', 2022, 12, 'Phuket 3006'),
('fv_055', 'fl_049', 'VAN', 'Toyota', 'Commuter', 2021, 12, 'Chiang Rai 49001'),
('fv_056', 'fl_050', 'VAN', 'Toyota', 'Commuter', 2023, 12, 'Chiang Mai 1006');

INSERT INTO fl_languages (fl_language_id, fl_id, fl_language_name) VALUES
('fll_001', 'fl_001', 'English'), ('fll_002', 'fl_001', 'Thai'), ('fll_003', 'fl_001', 'Mandarin'),
('fll_004', 'fl_002', 'English'), ('fll_005', 'fl_002', 'Thai'),
('fll_006', 'fl_003', 'English'), ('fll_007', 'fl_003', 'Thai'), ('fll_008', 'fl_003', 'Japanese'),
('fll_009', 'fl_004', 'English'), ('fll_010', 'fl_004', 'Thai'),
('fll_011', 'fl_005', 'English'), ('fll_012', 'fl_005', 'Thai'), ('fll_013', 'fl_005', 'Korean'),
('fll_014', 'fl_006', 'English'), ('fll_015', 'fl_006', 'Thai'),
('fll_016', 'fl_007', 'English'), ('fll_017', 'fl_007', 'Thai'), ('fll_018', 'fl_007', 'Russian'),
('fll_019', 'fl_008', 'English'), ('fll_020', 'fl_008', 'Thai'), ('fll_021', 'fl_008', 'French'),
('fll_022', 'fl_009', 'English'), ('fll_023', 'fl_009', 'Thai'),
('fll_024', 'fl_010', 'English'), ('fll_025', 'fl_010', 'Thai'), ('fll_026', 'fl_010', 'Mandarin'),
('fll_027', 'fl_011', 'English'), ('fll_028', 'fl_011', 'Thai'),
('fll_029', 'fl_012', 'English'), ('fll_030', 'fl_012', 'Thai'), ('fll_031', 'fl_012', 'Malay'),
('fll_032', 'fl_013', 'English'), ('fll_033', 'fl_013', 'Thai'),
('fll_034', 'fl_014', 'English'), ('fll_035', 'fl_014', 'Thai'), ('fll_036', 'fl_014', 'German'),
('fll_037', 'fl_015', 'English'), ('fll_038', 'fl_015', 'Thai'),
('fll_039', 'fl_016', 'English'), ('fll_040', 'fl_016', 'Thai'), ('fll_041', 'fl_016', 'French'),
('fll_042', 'fl_017', 'English'), ('fll_043', 'fl_017', 'Thai'),
('fll_044', 'fl_018', 'English'), ('fll_045', 'fl_018', 'Thai'), ('fll_046', 'fl_018', 'Japanese'),
('fll_047', 'fl_019', 'English'), ('fll_048', 'fl_019', 'Thai'),
('fll_049', 'fl_020', 'English'), ('fll_050', 'fl_020', 'Thai'), ('fll_051', 'fl_020', 'Mandarin'),
('fll_052', 'fl_021', 'English'), ('fll_053', 'fl_021', 'Thai'),
('fll_054', 'fl_022', 'English'), ('fll_055', 'fl_022', 'Thai'), ('fll_056', 'fl_022', 'Italian'),
('fll_057', 'fl_023', 'English'), ('fll_058', 'fl_023', 'Thai'),
('fll_059', 'fl_024', 'English'), ('fll_060', 'fl_024', 'Thai'), ('fll_061', 'fl_024', 'German'),
('fll_062', 'fl_025', 'English'), ('fll_063', 'fl_025', 'Thai'),
('fll_064', 'fl_026', 'English'), ('fll_065', 'fl_026', 'Thai'), ('fll_066', 'fl_026', 'Malay'),
('fll_067', 'fl_027', 'English'), ('fll_068', 'fl_027', 'Thai'),
('fll_069', 'fl_028', 'English'), ('fll_070', 'fl_028', 'Thai'), ('fll_071', 'fl_028', 'French'),
('fll_072', 'fl_029', 'English'), ('fll_073', 'fl_029', 'Thai'),
('fll_074', 'fl_030', 'English'), ('fll_075', 'fl_030', 'Thai'), ('fll_076', 'fl_030', 'Mandarin'),
('fll_077', 'fl_031', 'English'), ('fll_078', 'fl_031', 'Thai'),
('fll_079', 'fl_032', 'English'), ('fll_080', 'fl_032', 'Thai'), ('fll_081', 'fl_032', 'Korean'),
('fll_082', 'fl_033', 'English'), ('fll_083', 'fl_033', 'Thai'),
('fll_084', 'fl_034', 'English'), ('fll_085', 'fl_034', 'Thai'), ('fll_086', 'fl_034', 'Japanese'),
('fll_087', 'fl_035', 'English'), ('fll_088', 'fl_035', 'Thai'),
('fll_089', 'fl_036', 'English'), ('fll_090', 'fl_036', 'Thai'), ('fll_091', 'fl_036', 'French'),
('fll_092', 'fl_037', 'English'), ('fll_093', 'fl_037', 'Thai'),
('fll_094', 'fl_038', 'English'), ('fll_095', 'fl_038', 'Thai'), ('fll_096', 'fl_038', 'Mandarin'),
('fll_097', 'fl_039', 'English'), ('fll_098', 'fl_039', 'Thai'),
('fll_099', 'fl_040', 'English'), ('fll_100', 'fl_040', 'Thai'), ('fll_101', 'fl_040', 'German'),
('fll_102', 'fl_041', 'English'), ('fll_103', 'fl_041', 'Thai'),
('fll_104', 'fl_042', 'English'), ('fll_105', 'fl_042', 'Thai'), ('fll_106', 'fl_042', 'Italian'),
('fll_107', 'fl_043', 'English'), ('fll_108', 'fl_043', 'Thai'),
('fll_109', 'fl_044', 'English'), ('fll_110', 'fl_044', 'Thai'), ('fll_111', 'fl_044', 'Korean'),
('fll_112', 'fl_045', 'English'), ('fll_113', 'fl_045', 'Thai'),
('fll_114', 'fl_046', 'English'), ('fll_115', 'fl_046', 'Thai'), ('fll_116', 'fl_046', 'Japanese'),
('fll_117', 'fl_047', 'English'), ('fll_118', 'fl_047', 'Thai'),
('fll_119', 'fl_048', 'English'), ('fll_120', 'fl_048', 'Thai'), ('fll_121', 'fl_048', 'Russian'),
('fll_122', 'fl_049', 'English'), ('fll_123', 'fl_049', 'Thai'),
('fll_124', 'fl_050', 'English'), ('fll_125', 'fl_050', 'Thai'), ('fll_126', 'fl_050', 'Mandarin');

INSERT INTO fl_pickup_areas (fl_area_id, fl_id, fl_area_name) VALUES
('fpa_001', 'fl_001', 'Chiang Mai'), ('fpa_002', 'fl_001', 'Chiang Rai'),
('fpa_003', 'fl_002', 'Bangkok'),
('fpa_004', 'fl_003', 'Phuket'), ('fpa_005', 'fl_003', 'Krabi'),
('fpa_006', 'fl_004', 'Chiang Rai'), ('fpa_007', 'fl_004', 'Chiang Mai'),
('fpa_008', 'fl_005', 'Bangkok'), ('fpa_009', 'fl_005', 'Nonthaburi'),
('fpa_010', 'fl_006', 'Nakhon Ratchasima'),
('fpa_011', 'fl_007', 'Phuket'), ('fpa_012', 'fl_007', 'Phang Nga'),
('fpa_013', 'fl_008', 'Surat Thani'), ('fpa_014', 'fl_008', 'Koh Samui'),
('fpa_015', 'fl_009', 'Chiang Rai'),
('fpa_016', 'fl_010', 'Chiang Mai'), ('fpa_017', 'fl_010', 'Lamphun'),
('fpa_018', 'fl_011', 'Bangkok'), ('fpa_019', 'fl_011', 'Pathum Thani'), ('fpa_020', 'fl_011', 'Nonthaburi'),
('fpa_021', 'fl_012', 'Songkhla'), ('fpa_022', 'fl_012', 'Satun'),
('fpa_023', 'fl_013', 'Udon Thani'),
('fpa_024', 'fl_014', 'Surat Thani'), ('fpa_025', 'fl_014', 'Nakhon Si Thammarat'),
('fpa_026', 'fl_015', 'Bangkok'), ('fpa_027', 'fl_015', 'Samut Prakan'),
('fpa_028', 'fl_016', 'Krabi'), ('fpa_029', 'fl_016', 'Trang'),
('fpa_030', 'fl_017', 'Chonburi'), ('fpa_031', 'fl_017', 'Rayong'),
('fpa_032', 'fl_018', 'Lampang'),
('fpa_033', 'fl_019', 'Bangkok'), ('fpa_034', 'fl_019', 'Bangkok'), ('fpa_035', 'fl_019', 'Nonthaburi'),
('fpa_036', 'fl_020', 'Loei'),
('fpa_037', 'fl_021', 'Nonthaburi'), ('fpa_038', 'fl_021', 'Bangkok'),
('fpa_039', 'fl_022', 'Ayutthaya'), ('fpa_040', 'fl_022', 'Ang Thong'),
('fpa_041', 'fl_023', 'Bangkok'), ('fpa_042', 'fl_023', 'Samut Prakan'), ('fpa_043', 'fl_023', 'Pathum Thani'),
('fpa_044', 'fl_024', 'Phuket'), ('fpa_045', 'fl_024', 'Phang Nga'),
('fpa_046', 'fl_025', 'Chiang Mai'),
('fpa_047', 'fl_026', 'Songkhla'), ('fpa_048', 'fl_026', 'Pattani'),
('fpa_049', 'fl_027', 'Khon Kaen'), ('fpa_050', 'fl_027', 'Maha Sarakham'),
('fpa_051', 'fl_028', 'Chonburi'), ('fpa_052', 'fl_028', 'Rayong'),
('fpa_053', 'fl_029', 'Bangkok'),
('fpa_054', 'fl_030', 'Loei'), ('fpa_055', 'fl_030', 'Nong Khai'),
('fpa_056', 'fl_031', 'Udon Thani'), ('fpa_057', 'fl_031', 'Nong Khai'),
('fpa_058', 'fl_032', 'Chiang Mai'),
('fpa_059', 'fl_033', 'Chonburi'), ('fpa_060', 'fl_033', 'Pattaya'),
('fpa_061', 'fl_034', 'Chiang Rai'), ('fpa_062', 'fl_034', 'Phayao'),
('fpa_063', 'fl_035', 'Phuket'),
('fpa_064', 'fl_036', 'Krabi'), ('fpa_065', 'fl_036', 'Trang'), ('fpa_066', 'fl_036', 'Satun'),
('fpa_067', 'fl_037', 'Bangkok'),
('fpa_068', 'fl_038', 'Lampang'), ('fpa_069', 'fl_038', 'Lamphun'),
('fpa_070', 'fl_039', 'Songkhla'), ('fpa_071', 'fl_039', 'Nakhon Si Thammarat'),
('fpa_072', 'fl_040', 'Nonthaburi'), ('fpa_073', 'fl_040', 'Bangkok'),
('fpa_074', 'fl_041', 'Surat Thani'),
('fpa_075', 'fl_042', 'Ayutthaya'), ('fpa_076', 'fl_042', 'Lopburi'),
('fpa_077', 'fl_043', 'Phetchaburi'),
('fpa_078', 'fl_044', 'Khon Kaen'), ('fpa_079', 'fl_044', 'Kalasin'),
('fpa_080', 'fl_045', 'Chiang Rai'), ('fpa_081', 'fl_045', 'Phayao'),
('fpa_082', 'fl_046', 'Chonburi'), ('fpa_083', 'fl_046', 'Rayong'),
('fpa_084', 'fl_047', 'Bangkok'),
('fpa_085', 'fl_048', 'Phuket'), ('fpa_086', 'fl_048', 'Phang Nga'),
('fpa_087', 'fl_049', 'Chiang Rai'),
('fpa_088', 'fl_050', 'Chiang Mai'), ('fpa_089', 'fl_050', 'Chiang Rai');

INSERT INTO fl_availability (fl_available_id, fl_id, fl_available_start_date, fl_available_end_date, is_active) VALUES
('fav_001', 'fl_001', '2026-01-01', '2026-12-31', true),
('fav_002', 'fl_002', '2026-01-01', '2026-12-31', true),
('fav_003', 'fl_003', '2026-01-01', '2026-12-31', true),
('fav_004', 'fl_004', '2026-02-01', '2026-11-30', true),
('fav_005', 'fl_005', '2026-01-01', '2026-12-31', true),
('fav_006', 'fl_006', '2026-01-01', '2026-12-31', true),
('fav_007', 'fl_007', '2025-06-01', '2025-12-31', false),
('fav_008', 'fl_008', '2026-01-01', '2026-12-31', true),
('fav_009', 'fl_009', '2026-01-01', '2026-12-31', true),
('fav_010', 'fl_010', '2026-01-01', '2026-10-31', true),
('fav_011', 'fl_011', '2026-01-01', '2026-12-31', true),
('fav_012', 'fl_012', '2026-01-01', '2026-12-31', true),
('fav_013', 'fl_013', '2025-07-01', '2025-12-31', false),
('fav_014', 'fl_014', '2026-01-01', '2026-12-31', true),
('fav_015', 'fl_015', '2025-09-01', '2025-12-31', false),
('fav_016', 'fl_016', '2026-01-01', '2026-12-31', true),
('fav_017', 'fl_017', '2026-01-01', '2026-12-31', true),
('fav_018', 'fl_018', '2025-08-01', '2025-12-31', false),
('fav_019', 'fl_019', '2026-01-01', '2026-12-31', true),
('fav_020', 'fl_020', '2025-10-01', '2025-12-31', false),
('fav_021', 'fl_021', '2026-01-01', '2026-12-31', true),
('fav_022', 'fl_022', '2026-01-01', '2026-12-31', true),
('fav_023', 'fl_023', '2026-01-01', '2026-12-31', true),
('fav_024', 'fl_024', '2026-02-01', '2026-12-31', true),
('fav_025', 'fl_025', '2026-01-01', '2026-09-30', true),
('fav_026', 'fl_026', '2026-01-01', '2026-12-31', true),
('fav_027', 'fl_027', '2026-01-01', '2026-12-31', true),
('fav_028', 'fl_028', '2026-01-01', '2026-12-31', true),
('fav_029', 'fl_029', '2025-11-01', '2025-12-31', false),
('fav_030', 'fl_030', '2026-01-01', '2026-12-31', true),
('fav_031', 'fl_031', '2026-01-01', '2026-12-31', true),
('fav_032', 'fl_032', '2026-01-01', '2026-12-31', true),
('fav_033', 'fl_033', '2026-01-01', '2026-12-31', true),
('fav_034', 'fl_034', '2026-01-01', '2026-12-31', true),
('fav_035', 'fl_035', '2025-10-01', '2025-12-31', false),
('fav_036', 'fl_036', '2026-01-01', '2026-12-31', true),
('fav_037', 'fl_037', '2026-01-01', '2026-12-31', true),
('fav_038', 'fl_038', '2026-01-01', '2026-11-30', true),
('fav_039', 'fl_039', '2026-01-01', '2026-12-31', true),
('fav_040', 'fl_040', '2026-01-01', '2026-12-31', true),
('fav_041', 'fl_041', '2026-01-01', '2026-10-31', true),
('fav_042', 'fl_042', '2026-01-01', '2026-12-31', true),
('fav_043', 'fl_043', '2025-12-01', '2025-12-31', false),
('fav_044', 'fl_044', '2026-01-01', '2026-12-31', true),
('fav_045', 'fl_045', '2026-01-01', '2026-12-31', true),
('fav_046', 'fl_046', '2026-01-01', '2026-12-31', true),
('fav_047', 'fl_047', '2025-10-01', '2025-12-31', false),
('fav_048', 'fl_048', '2026-01-01', '2026-12-31', true),
('fav_049', 'fl_049', '2026-01-01', '2026-12-31', true),
('fav_050', 'fl_050', '2026-01-01', '2026-12-31', true);

INSERT INTO fl_documents (fl_doc_id, fl_id, fl_vehicle_id, fl_doc_type, file_url, fl_doc_status, is_latest, fl_uploaded_at, reviewed_by, reviewed_at) VALUES
('fld_001', 'fl_001', NULL, 'ID_CARD', 'https://example.com/docs/fl_001_id.pdf', 'APPROVED', true, '2025-01-22 09:00:00', 'ad_001', '2025-01-28 10:00:00'),
('fld_002', 'fl_001', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_001_dl.pdf', 'APPROVED', true, '2025-01-22 09:30:00', 'ad_001', '2025-01-28 10:30:00'),
('fld_003', 'fl_001', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_001_pdl.pdf', 'APPROVED', true, '2025-01-22 10:00:00', 'ad_001', '2025-01-28 11:00:00'),
('fld_004', 'fl_001', 'fv_001', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_001_vreg_fv001.pdf', 'APPROVED', true, '2025-01-22 10:30:00', 'ad_001', '2025-01-28 11:30:00'),
('fld_005', 'fl_001', 'fv_001', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_001_vins_fv001.pdf', 'APPROVED', true, '2025-01-22 11:00:00', 'ad_001', '2025-01-28 12:00:00'),
('fld_006', 'fl_001', 'fv_002', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_001_vreg_fv002.pdf', 'APPROVED', true, '2025-01-22 11:30:00', 'ad_001', '2025-01-28 12:30:00'),
('fld_007', 'fl_001', 'fv_002', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_001_vins_fv002.pdf', 'APPROVED', true, '2025-01-22 12:00:00', 'ad_001', '2025-01-28 13:00:00'),
('fld_008', 'fl_002', NULL, 'ID_CARD', 'https://example.com/docs/fl_002_id.pdf', 'APPROVED', true, '2025-01-27 09:00:00', 'ad_002', '2025-02-02 10:00:00'),
('fld_009', 'fl_002', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_002_dl.pdf', 'APPROVED', true, '2025-01-27 09:30:00', 'ad_002', '2025-02-02 10:30:00'),
('fld_010', 'fl_002', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_002_pdl.pdf', 'APPROVED', true, '2025-01-27 10:00:00', 'ad_002', '2025-02-02 11:00:00'),
('fld_011', 'fl_002', 'fv_003', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_002_vreg_fv003.pdf', 'APPROVED', true, '2025-01-27 10:30:00', 'ad_002', '2025-02-02 11:30:00'),
('fld_012', 'fl_002', 'fv_003', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_002_vins_fv003.pdf', 'APPROVED', true, '2025-01-27 11:00:00', 'ad_002', '2025-02-02 12:00:00'),
('fld_013', 'fl_003', NULL, 'ID_CARD', 'https://example.com/docs/fl_003_id.pdf', 'APPROVED', true, '2025-02-03 09:00:00', 'ad_003', '2025-02-09 10:00:00'),
('fld_014', 'fl_003', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_003_dl.pdf', 'APPROVED', true, '2025-02-03 09:30:00', 'ad_003', '2025-02-09 10:30:00'),
('fld_015', 'fl_003', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_003_pdl.pdf', 'APPROVED', true, '2025-02-03 10:00:00', 'ad_003', '2025-02-09 11:00:00'),
('fld_016', 'fl_003', 'fv_004', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_003_vreg_fv004.pdf', 'APPROVED', true, '2025-02-03 10:30:00', 'ad_003', '2025-02-09 11:30:00'),
('fld_017', 'fl_003', 'fv_004', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_003_vins_fv004.pdf', 'APPROVED', true, '2025-02-03 11:00:00', 'ad_003', '2025-02-09 12:00:00'),
('fld_018', 'fl_004', NULL, 'ID_CARD', 'https://example.com/docs/fl_004_id.pdf', 'PENDING', true, '2025-02-12 09:00:00', NULL, NULL),
('fld_019', 'fl_004', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_004_dl.pdf', 'PENDING', true, '2025-02-12 09:30:00', NULL, NULL),
('fld_020', 'fl_004', 'fv_005', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_004_vreg_fv005.pdf', 'PENDING', true, '2025-02-12 10:00:00', NULL, NULL),
('fld_021', 'fl_004', 'fv_005', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_004_vins_fv005.pdf', 'PENDING', true, '2025-02-12 10:30:00', NULL, NULL),
('fld_022', 'fl_005', NULL, 'ID_CARD', 'https://example.com/docs/fl_005_id.pdf', 'APPROVED', true, '2025-02-17 09:00:00', 'ad_001', '2025-02-23 10:00:00'),
('fld_023', 'fl_005', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_005_dl.pdf', 'APPROVED', true, '2025-02-17 09:30:00', 'ad_001', '2025-02-23 10:30:00'),
('fld_024', 'fl_005', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_005_pdl.pdf', 'APPROVED', true, '2025-02-17 10:00:00', 'ad_001', '2025-02-23 11:00:00'),
('fld_025', 'fl_005', 'fv_006', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_005_vreg_fv006.pdf', 'APPROVED', true, '2025-02-17 10:30:00', 'ad_001', '2025-02-23 11:30:00'),
('fld_026', 'fl_005', 'fv_006', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_005_vins_fv006.pdf', 'APPROVED', true, '2025-02-17 11:00:00', 'ad_001', '2025-02-23 12:00:00'),
('fld_027', 'fl_006', NULL, 'ID_CARD', 'https://example.com/docs/fl_006_id.pdf', 'APPROVED', true, '2025-03-03 09:00:00', 'ad_002', '2025-03-09 10:00:00'),
('fld_028', 'fl_006', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_006_dl.pdf', 'APPROVED', true, '2025-03-03 09:30:00', 'ad_002', '2025-03-09 10:30:00'),
('fld_029', 'fl_006', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_006_pdl.pdf', 'APPROVED', true, '2025-03-03 10:00:00', 'ad_002', '2025-03-09 11:00:00'),
('fld_030', 'fl_006', 'fv_007', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_006_vreg_fv007.pdf', 'APPROVED', true, '2025-03-03 10:30:00', 'ad_002', '2025-03-09 11:30:00'),
('fld_031', 'fl_006', 'fv_007', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_006_vins_fv007.pdf', 'APPROVED', true, '2025-03-03 11:00:00', 'ad_002', '2025-03-09 12:00:00'),
('fld_032', 'fl_007', NULL, 'ID_CARD', 'https://example.com/docs/fl_007_id_v1.pdf', 'REJECTED', false, '2025-03-12 09:00:00', 'ad_003', '2025-03-18 10:00:00'),
('fld_033', 'fl_007', NULL, 'ID_CARD', 'https://example.com/docs/fl_007_id_v2.pdf', 'REJECTED', true, '2025-04-01 09:00:00', 'ad_003', '2025-04-07 10:00:00'),
('fld_034', 'fl_007', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_007_dl.pdf', 'REJECTED', true, '2025-03-12 09:30:00', 'ad_003', '2025-03-18 10:30:00'),
('fld_035', 'fl_007', 'fv_008', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_007_vreg_fv008.pdf', 'REJECTED', true, '2025-03-12 10:00:00', 'ad_003', '2025-03-18 11:00:00'),
('fld_036', 'fl_007', 'fv_008', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_007_vins_fv008.pdf', 'REJECTED', true, '2025-03-12 10:30:00', 'ad_003', '2025-03-18 11:30:00'),
('fld_037', 'fl_008', NULL, 'ID_CARD', 'https://example.com/docs/fl_008_id.pdf', 'APPROVED', true, '2025-03-17 09:00:00', 'ad_001', '2025-03-23 10:00:00'),
('fld_038', 'fl_008', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_008_dl.pdf', 'APPROVED', true, '2025-03-17 09:30:00', 'ad_001', '2025-03-23 10:30:00'),
('fld_039', 'fl_008', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_008_pdl.pdf', 'APPROVED', true, '2025-03-17 10:00:00', 'ad_001', '2025-03-23 11:00:00'),
('fld_040', 'fl_008', 'fv_010', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_008_vreg_fv010.pdf', 'APPROVED', true, '2025-03-17 10:30:00', 'ad_001', '2025-03-23 11:30:00'),
('fld_041', 'fl_008', 'fv_010', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_008_vins_fv010.pdf', 'APPROVED', true, '2025-03-17 11:00:00', 'ad_001', '2025-03-23 12:00:00'),
('fld_042', 'fl_009', NULL, 'ID_CARD', 'https://example.com/docs/fl_009_id.pdf', 'APPROVED', true, '2025-04-03 09:00:00', 'ad_002', '2025-04-09 10:00:00'),
('fld_043', 'fl_009', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_009_dl.pdf', 'APPROVED', true, '2025-04-03 09:30:00', 'ad_002', '2025-04-09 10:30:00'),
('fld_044', 'fl_009', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_009_pdl.pdf', 'APPROVED', true, '2025-04-03 10:00:00', 'ad_002', '2025-04-09 11:00:00'),
('fld_045', 'fl_009', 'fv_011', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_009_vreg_fv011.pdf', 'APPROVED', true, '2025-04-03 10:30:00', 'ad_002', '2025-04-09 11:30:00'),
('fld_046', 'fl_009', 'fv_011', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_009_vins_fv011.pdf', 'APPROVED', true, '2025-04-03 11:00:00', 'ad_002', '2025-04-09 12:00:00'),
('fld_047', 'fl_010', NULL, 'ID_CARD', 'https://example.com/docs/fl_010_id.pdf', 'PENDING', true, '2025-04-12 09:00:00', NULL, NULL),
('fld_048', 'fl_010', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_010_dl.pdf', 'PENDING', true, '2025-04-12 09:30:00', NULL, NULL),
('fld_049', 'fl_010', 'fv_012', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_010_vreg_fv012.pdf', 'PENDING', true, '2025-04-12 10:00:00', NULL, NULL),
('fld_050', 'fl_010', 'fv_012', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_010_vins_fv012.pdf', 'PENDING', true, '2025-04-12 10:30:00', NULL, NULL),
('fld_051', 'fl_011', NULL, 'ID_CARD', 'https://example.com/docs/fl_011_id.pdf', 'APPROVED', true, '2025-01-12 09:00:00', 'ad_003', '2025-01-18 10:00:00'),
('fld_052', 'fl_011', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_011_dl.pdf', 'APPROVED', true, '2025-01-12 09:30:00', 'ad_003', '2025-01-18 10:30:00'),
('fld_053', 'fl_011', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_011_pdl.pdf', 'APPROVED', true, '2025-01-12 10:00:00', 'ad_003', '2025-01-18 11:00:00'),
('fld_054', 'fl_011', 'fv_013', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_011_vreg_fv013.pdf', 'APPROVED', true, '2025-01-12 10:30:00', 'ad_003', '2025-01-18 11:30:00'),
('fld_055', 'fl_011', 'fv_013', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_011_vins_fv013.pdf', 'APPROVED', true, '2025-01-12 11:00:00', 'ad_003', '2025-01-18 12:00:00'),
('fld_056', 'fl_011', 'fv_014', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_011_vreg_fv014.pdf', 'APPROVED', true, '2025-01-12 11:30:00', 'ad_003', '2025-01-18 12:30:00'),
('fld_057', 'fl_011', 'fv_014', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_011_vins_fv014.pdf', 'APPROVED', true, '2025-01-12 12:00:00', 'ad_003', '2025-01-18 13:00:00'),
('fld_058', 'fl_012', NULL, 'ID_CARD', 'https://example.com/docs/fl_012_id.pdf', 'APPROVED', true, '2025-04-22 09:00:00', 'ad_001', '2025-04-28 10:00:00'),
('fld_059', 'fl_012', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_012_dl.pdf', 'APPROVED', true, '2025-04-22 09:30:00', 'ad_001', '2025-04-28 10:30:00'),
('fld_060', 'fl_012', 'fv_015', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_012_vreg_fv015.pdf', 'APPROVED', true, '2025-04-22 10:00:00', 'ad_001', '2025-04-28 11:00:00'),
('fld_061', 'fl_012', 'fv_015', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_012_vins_fv015.pdf', 'APPROVED', true, '2025-04-22 10:30:00', 'ad_001', '2025-04-28 11:30:00'),
('fld_062', 'fl_013', NULL, 'ID_CARD', 'https://example.com/docs/fl_013_id.pdf', 'REJECTED', true, '2025-05-03 09:00:00', 'ad_002', '2025-05-09 10:00:00'),
('fld_063', 'fl_013', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_013_dl.pdf', 'REJECTED', true, '2025-05-03 09:30:00', 'ad_002', '2025-05-09 10:30:00'),
('fld_064', 'fl_013', 'fv_016', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_013_vreg_fv016.pdf', 'REJECTED', true, '2025-05-03 10:00:00', 'ad_002', '2025-05-09 11:00:00'),
('fld_065', 'fl_013', 'fv_016', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_013_vins_fv016.pdf', 'REJECTED', true, '2025-05-03 10:30:00', 'ad_002', '2025-05-09 11:30:00'),
('fld_066', 'fl_014', NULL, 'ID_CARD', 'https://example.com/docs/fl_014_id.pdf', 'APPROVED', true, '2025-05-12 09:00:00', 'ad_003', '2025-05-18 10:00:00'),
('fld_067', 'fl_014', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_014_dl.pdf', 'APPROVED', true, '2025-05-12 09:30:00', 'ad_003', '2025-05-18 10:30:00'),
('fld_068', 'fl_014', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_014_pdl.pdf', 'APPROVED', true, '2025-05-12 10:00:00', 'ad_003', '2025-05-18 11:00:00'),
('fld_069', 'fl_014', 'fv_017', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_014_vreg_fv017.pdf', 'APPROVED', true, '2025-05-12 10:30:00', 'ad_003', '2025-05-18 11:30:00'),
('fld_070', 'fl_014', 'fv_017', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_014_vins_fv017.pdf', 'APPROVED', true, '2025-05-12 11:00:00', 'ad_003', '2025-05-18 12:00:00'),
('fld_071', 'fl_015', NULL, 'ID_CARD', 'https://example.com/docs/fl_015_id.pdf', 'PENDING', true, '2025-05-22 09:00:00', NULL, NULL),
('fld_072', 'fl_015', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_015_dl.pdf', 'PENDING', true, '2025-05-22 09:30:00', NULL, NULL),
('fld_073', 'fl_015', 'fv_018', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_015_vreg_fv018.pdf', 'PENDING', true, '2025-05-22 10:00:00', NULL, NULL),
('fld_074', 'fl_015', 'fv_018', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_015_vins_fv018.pdf', 'PENDING', true, '2025-05-22 10:30:00', NULL, NULL),
('fld_075', 'fl_016', NULL, 'ID_CARD', 'https://example.com/docs/fl_016_id.pdf', 'APPROVED', true, '2025-06-03 09:00:00', 'ad_001', '2025-06-09 10:00:00'),
('fld_076', 'fl_016', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_016_dl.pdf', 'APPROVED', true, '2025-06-03 09:30:00', 'ad_001', '2025-06-09 10:30:00'),
('fld_077', 'fl_016', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_016_pdl.pdf', 'APPROVED', true, '2025-06-03 10:00:00', 'ad_001', '2025-06-09 11:00:00'),
('fld_078', 'fl_016', 'fv_019', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_016_vreg_fv019.pdf', 'APPROVED', true, '2025-06-03 10:30:00', 'ad_001', '2025-06-09 11:30:00'),
('fld_079', 'fl_016', 'fv_019', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_016_vins_fv019.pdf', 'APPROVED', true, '2025-06-03 11:00:00', 'ad_001', '2025-06-09 12:00:00'),
('fld_080', 'fl_017', NULL, 'ID_CARD', 'https://example.com/docs/fl_017_id.pdf', 'APPROVED', true, '2025-06-12 09:00:00', 'ad_002', '2025-06-18 10:00:00'),
('fld_081', 'fl_017', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_017_dl.pdf', 'APPROVED', true, '2025-06-12 09:30:00', 'ad_002', '2025-06-18 10:30:00'),
('fld_082', 'fl_017', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_017_pdl.pdf', 'APPROVED', true, '2025-06-12 10:00:00', 'ad_002', '2025-06-18 11:00:00'),
('fld_083', 'fl_017', 'fv_020', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_017_vreg_fv020.pdf', 'APPROVED', true, '2025-06-12 10:30:00', 'ad_002', '2025-06-18 11:30:00'),
('fld_084', 'fl_017', 'fv_020', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_017_vins_fv020.pdf', 'APPROVED', true, '2025-06-12 11:00:00', 'ad_002', '2025-06-18 12:00:00'),
('fld_085', 'fl_018', NULL, 'ID_CARD', 'https://example.com/docs/fl_018_id.pdf', 'REJECTED', true, '2025-06-22 09:00:00', 'ad_003', '2025-06-28 10:00:00'),
('fld_086', 'fl_018', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_018_dl.pdf', 'REJECTED', true, '2025-06-22 09:30:00', 'ad_003', '2025-06-28 10:30:00'),
('fld_087', 'fl_018', 'fv_022', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_018_vreg_fv022.pdf', 'REJECTED', true, '2025-06-22 10:00:00', 'ad_003', '2025-06-28 11:00:00'),
('fld_088', 'fl_018', 'fv_022', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_018_vins_fv022.pdf', 'REJECTED', true, '2025-06-22 10:30:00', 'ad_003', '2025-06-28 11:30:00'),
('fld_089', 'fl_019', NULL, 'ID_CARD', 'https://example.com/docs/fl_019_id.pdf', 'APPROVED', true, '2025-07-03 09:00:00', 'ad_001', '2025-07-09 10:00:00'),
('fld_090', 'fl_019', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_019_dl.pdf', 'APPROVED', true, '2025-07-03 09:30:00', 'ad_001', '2025-07-09 10:30:00'),
('fld_091', 'fl_019', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_019_pdl.pdf', 'APPROVED', true, '2025-07-03 10:00:00', 'ad_001', '2025-07-09 11:00:00'),
('fld_092', 'fl_019', 'fv_023', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_019_vreg_fv023.pdf', 'APPROVED', true, '2025-07-03 10:30:00', 'ad_001', '2025-07-09 11:30:00'),
('fld_093', 'fl_019', 'fv_023', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_019_vins_fv023.pdf', 'APPROVED', true, '2025-07-03 11:00:00', 'ad_001', '2025-07-09 12:00:00'),
('fld_094', 'fl_020', NULL, 'ID_CARD', 'https://example.com/docs/fl_020_id.pdf', 'PENDING', true, '2025-07-12 09:00:00', NULL, NULL),
('fld_095', 'fl_020', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_020_dl.pdf', 'PENDING', true, '2025-07-12 09:30:00', NULL, NULL),
('fld_096', 'fl_020', 'fv_024', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_020_vreg_fv024.pdf', 'PENDING', true, '2025-07-12 10:00:00', NULL, NULL),
('fld_097', 'fl_020', 'fv_024', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_020_vins_fv024.pdf', 'PENDING', true, '2025-07-12 10:30:00', NULL, NULL),
('fld_098', 'fl_021', NULL, 'ID_CARD', 'https://example.com/docs/fl_021_id.pdf', 'APPROVED', true, '2025-07-17 09:00:00', 'ad_002', '2025-07-23 10:00:00'),
('fld_099', 'fl_021', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_021_dl.pdf', 'APPROVED', true, '2025-07-17 09:30:00', 'ad_002', '2025-07-23 10:30:00'),
('fld_100', 'fl_021', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_021_pdl.pdf', 'APPROVED', true, '2025-07-17 10:00:00', 'ad_002', '2025-07-23 11:00:00'),
('fld_101', 'fl_021', 'fv_025', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_021_vreg_fv025.pdf', 'APPROVED', true, '2025-07-17 10:30:00', 'ad_002', '2025-07-23 11:30:00'),
('fld_102', 'fl_021', 'fv_025', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_021_vins_fv025.pdf', 'APPROVED', true, '2025-07-17 11:00:00', 'ad_002', '2025-07-23 12:00:00'),
('fld_103', 'fl_022', NULL, 'ID_CARD', 'https://example.com/docs/fl_022_id.pdf', 'APPROVED', true, '2025-07-22 09:00:00', 'ad_003', '2025-07-28 10:00:00'),
('fld_104', 'fl_022', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_022_dl.pdf', 'APPROVED', true, '2025-07-22 09:30:00', 'ad_003', '2025-07-28 10:30:00'),
('fld_105', 'fl_022', 'fv_026', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_022_vreg_fv026.pdf', 'APPROVED', true, '2025-07-22 10:00:00', 'ad_003', '2025-07-28 11:00:00'),
('fld_106', 'fl_022', 'fv_026', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_022_vins_fv026.pdf', 'APPROVED', true, '2025-07-22 10:30:00', 'ad_003', '2025-07-28 11:30:00'),
('fld_107', 'fl_023', NULL, 'ID_CARD', 'https://example.com/docs/fl_023_id.pdf', 'APPROVED', true, '2025-08-03 09:00:00', 'ad_001', '2025-08-09 10:00:00'),
('fld_108', 'fl_023', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_023_dl.pdf', 'APPROVED', true, '2025-08-03 09:30:00', 'ad_001', '2025-08-09 10:30:00'),
('fld_109', 'fl_023', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_023_pdl.pdf', 'APPROVED', true, '2025-08-03 10:00:00', 'ad_001', '2025-08-09 11:00:00'),
('fld_110', 'fl_023', 'fv_027', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_023_vreg_fv027.pdf', 'APPROVED', true, '2025-08-03 10:30:00', 'ad_001', '2025-08-09 11:30:00'),
('fld_111', 'fl_023', 'fv_027', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_023_vins_fv027.pdf', 'APPROVED', true, '2025-08-03 11:00:00', 'ad_001', '2025-08-09 12:00:00'),
('fld_112', 'fl_023', 'fv_028', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_023_vreg_fv028.pdf', 'APPROVED', true, '2025-08-03 11:30:00', 'ad_001', '2025-08-09 12:30:00'),
('fld_113', 'fl_023', 'fv_028', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_023_vins_fv028.pdf', 'APPROVED', true, '2025-08-03 12:00:00', 'ad_001', '2025-08-09 13:00:00'),
('fld_114', 'fl_024', NULL, 'ID_CARD', 'https://example.com/docs/fl_024_id.pdf', 'PENDING', true, '2025-08-12 09:00:00', NULL, NULL),
('fld_115', 'fl_024', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_024_dl.pdf', 'PENDING', true, '2025-08-12 09:30:00', NULL, NULL),
('fld_116', 'fl_024', 'fv_029', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_024_vreg_fv029.pdf', 'PENDING', true, '2025-08-12 10:00:00', NULL, NULL),
('fld_117', 'fl_024', 'fv_029', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_024_vins_fv029.pdf', 'PENDING', true, '2025-08-12 10:30:00', NULL, NULL),
('fld_118', 'fl_025', NULL, 'ID_CARD', 'https://example.com/docs/fl_025_id.pdf', 'REJECTED', true, '2025-08-17 09:00:00', 'ad_002', '2025-08-23 10:00:00'),
('fld_119', 'fl_025', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_025_dl.pdf', 'REJECTED', true, '2025-08-17 09:30:00', 'ad_002', '2025-08-23 10:30:00'),
('fld_120', 'fl_025', 'fv_030', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_025_vreg_fv030.pdf', 'REJECTED', true, '2025-08-17 10:00:00', 'ad_002', '2025-08-23 11:00:00'),
('fld_121', 'fl_025', 'fv_030', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_025_vins_fv030.pdf', 'REJECTED', true, '2025-08-17 10:30:00', 'ad_002', '2025-08-23 11:30:00'),
('fld_122', 'fl_026', NULL, 'ID_CARD', 'https://example.com/docs/fl_026_id.pdf', 'APPROVED', true, '2025-08-22 09:00:00', 'ad_003', '2025-08-28 10:00:00'),
('fld_123', 'fl_026', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_026_dl.pdf', 'APPROVED', true, '2025-08-22 09:30:00', 'ad_003', '2025-08-28 10:30:00'),
('fld_124', 'fl_026', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_026_pdl.pdf', 'APPROVED', true, '2025-08-22 10:00:00', 'ad_003', '2025-08-28 11:00:00'),
('fld_125', 'fl_026', 'fv_031', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_026_vreg_fv031.pdf', 'APPROVED', true, '2025-08-22 10:30:00', 'ad_003', '2025-08-28 11:30:00'),
('fld_126', 'fl_026', 'fv_031', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_026_vins_fv031.pdf', 'APPROVED', true, '2025-08-22 11:00:00', 'ad_003', '2025-08-28 12:00:00'),
('fld_127', 'fl_027', NULL, 'ID_CARD', 'https://example.com/docs/fl_027_id.pdf', 'APPROVED', true, '2025-09-03 09:00:00', 'ad_001', '2025-09-09 10:00:00'),
('fld_128', 'fl_027', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_027_dl.pdf', 'APPROVED', true, '2025-09-03 09:30:00', 'ad_001', '2025-09-09 10:30:00'),
('fld_129', 'fl_027', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_027_pdl.pdf', 'APPROVED', true, '2025-09-03 10:00:00', 'ad_001', '2025-09-09 11:00:00'),
('fld_130', 'fl_027', 'fv_032', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_027_vreg_fv032.pdf', 'APPROVED', true, '2025-09-03 10:30:00', 'ad_001', '2025-09-09 11:30:00'),
('fld_131', 'fl_027', 'fv_032', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_027_vins_fv032.pdf', 'APPROVED', true, '2025-09-03 11:00:00', 'ad_001', '2025-09-09 12:00:00'),
('fld_132', 'fl_028', NULL, 'ID_CARD', 'https://example.com/docs/fl_028_id.pdf', 'APPROVED', true, '2025-09-07 09:00:00', 'ad_002', '2025-09-13 10:00:00'),
('fld_133', 'fl_028', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_028_dl.pdf', 'APPROVED', true, '2025-09-07 09:30:00', 'ad_002', '2025-09-13 10:30:00'),
('fld_134', 'fl_028', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_028_pdl.pdf', 'APPROVED', true, '2025-09-07 10:00:00', 'ad_002', '2025-09-13 11:00:00'),
('fld_135', 'fl_028', 'fv_033', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_028_vreg_fv033.pdf', 'APPROVED', true, '2025-09-07 10:30:00', 'ad_002', '2025-09-13 11:30:00'),
('fld_136', 'fl_028', 'fv_033', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_028_vins_fv033.pdf', 'APPROVED', true, '2025-09-07 11:00:00', 'ad_002', '2025-09-13 12:00:00'),
('fld_137', 'fl_029', NULL, 'ID_CARD', 'https://example.com/docs/fl_029_id.pdf', 'REJECTED', true, '2025-09-12 09:00:00', 'ad_003', '2025-09-18 10:00:00'),
('fld_138', 'fl_029', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_029_dl.pdf', 'REJECTED', true, '2025-09-12 09:30:00', 'ad_003', '2025-09-18 10:30:00'),
('fld_139', 'fl_029', 'fv_034', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_029_vreg_fv034.pdf', 'REJECTED', true, '2025-09-12 10:00:00', 'ad_003', '2025-09-18 11:00:00'),
('fld_140', 'fl_029', 'fv_034', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_029_vins_fv034.pdf', 'REJECTED', true, '2025-09-12 10:30:00', 'ad_003', '2025-09-18 11:30:00'),
('fld_141', 'fl_030', NULL, 'ID_CARD', 'https://example.com/docs/fl_030_id.pdf', 'PENDING', true, '2025-09-17 09:00:00', NULL, NULL),
('fld_142', 'fl_030', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_030_dl.pdf', 'PENDING', true, '2025-09-17 09:30:00', NULL, NULL),
('fld_143', 'fl_030', 'fv_035', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_030_vreg_fv035.pdf', 'PENDING', true, '2025-09-17 10:00:00', NULL, NULL),
('fld_144', 'fl_030', 'fv_035', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_030_vins_fv035.pdf', 'PENDING', true, '2025-09-17 10:30:00', NULL, NULL),
('fld_145', 'fl_031', NULL, 'ID_CARD', 'https://example.com/docs/fl_031_id.pdf', 'APPROVED', true, '2025-09-22 09:00:00', 'ad_001', '2025-09-28 10:00:00'),
('fld_146', 'fl_031', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_031_dl.pdf', 'APPROVED', true, '2025-09-22 09:30:00', 'ad_001', '2025-09-28 10:30:00'),
('fld_147', 'fl_031', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_031_pdl.pdf', 'APPROVED', true, '2025-09-22 10:00:00', 'ad_001', '2025-09-28 11:00:00'),
('fld_148', 'fl_031', 'fv_036', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_031_vreg_fv036.pdf', 'APPROVED', true, '2025-09-22 10:30:00', 'ad_001', '2025-09-28 11:30:00'),
('fld_149', 'fl_031', 'fv_036', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_031_vins_fv036.pdf', 'APPROVED', true, '2025-09-22 11:00:00', 'ad_001', '2025-09-28 12:00:00'),
('fld_150', 'fl_032', NULL, 'ID_CARD', 'https://example.com/docs/fl_032_id.pdf', 'APPROVED', true, '2025-10-03 09:00:00', 'ad_002', '2025-10-09 10:00:00'),
('fld_151', 'fl_032', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_032_dl.pdf', 'APPROVED', true, '2025-10-03 09:30:00', 'ad_002', '2025-10-09 10:30:00'),
('fld_152', 'fl_032', 'fv_037', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_032_vreg_fv037.pdf', 'APPROVED', true, '2025-10-03 10:00:00', 'ad_002', '2025-10-09 11:00:00'),
('fld_153', 'fl_032', 'fv_037', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_032_vins_fv037.pdf', 'APPROVED', true, '2025-10-03 10:30:00', 'ad_002', '2025-10-09 11:30:00'),
('fld_154', 'fl_033', NULL, 'ID_CARD', 'https://example.com/docs/fl_033_id.pdf', 'PENDING', true, '2025-10-10 09:00:00', NULL, NULL),
('fld_155', 'fl_033', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_033_dl.pdf', 'PENDING', true, '2025-10-10 09:30:00', NULL, NULL),
('fld_156', 'fl_033', 'fv_038', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_033_vreg_fv038.pdf', 'PENDING', true, '2025-10-10 10:00:00', NULL, NULL),
('fld_157', 'fl_033', 'fv_038', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_033_vins_fv038.pdf', 'PENDING', true, '2025-10-10 10:30:00', NULL, NULL),
('fld_158', 'fl_034', NULL, 'ID_CARD', 'https://example.com/docs/fl_034_id.pdf', 'APPROVED', true, '2025-10-17 09:00:00', 'ad_003', '2025-10-23 10:00:00'),
('fld_159', 'fl_034', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_034_dl.pdf', 'APPROVED', true, '2025-10-17 09:30:00', 'ad_003', '2025-10-23 10:30:00'),
('fld_160', 'fl_034', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_034_pdl.pdf', 'APPROVED', true, '2025-10-17 10:00:00', 'ad_003', '2025-10-23 11:00:00'),
('fld_161', 'fl_034', 'fv_039', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_034_vreg_fv039.pdf', 'APPROVED', true, '2025-10-17 10:30:00', 'ad_003', '2025-10-23 11:30:00'),
('fld_162', 'fl_034', 'fv_039', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_034_vins_fv039.pdf', 'APPROVED', true, '2025-10-17 11:00:00', 'ad_003', '2025-10-23 12:00:00'),
('fld_163', 'fl_035', NULL, 'ID_CARD', 'https://example.com/docs/fl_035_id.pdf', 'REJECTED', true, '2025-10-22 09:00:00', 'ad_001', '2025-10-28 10:00:00'),
('fld_164', 'fl_035', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_035_dl.pdf', 'REJECTED', true, '2025-10-22 09:30:00', 'ad_001', '2025-10-28 10:30:00'),
('fld_165', 'fl_035', 'fv_040', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_035_vreg_fv040.pdf', 'REJECTED', true, '2025-10-22 10:00:00', 'ad_001', '2025-10-28 11:00:00'),
('fld_166', 'fl_035', 'fv_040', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_035_vins_fv040.pdf', 'REJECTED', true, '2025-10-22 10:30:00', 'ad_001', '2025-10-28 11:30:00'),
('fld_167', 'fl_036', NULL, 'ID_CARD', 'https://example.com/docs/fl_036_id.pdf', 'APPROVED', true, '2025-11-03 09:00:00', 'ad_002', '2025-11-09 10:00:00'),
('fld_168', 'fl_036', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_036_dl.pdf', 'APPROVED', true, '2025-11-03 09:30:00', 'ad_002', '2025-11-09 10:30:00'),
('fld_169', 'fl_036', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_036_pdl.pdf', 'APPROVED', true, '2025-11-03 10:00:00', 'ad_002', '2025-11-09 11:00:00'),
('fld_170', 'fl_036', 'fv_041', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_036_vreg_fv041.pdf', 'APPROVED', true, '2025-11-03 10:30:00', 'ad_002', '2025-11-09 11:30:00'),
('fld_171', 'fl_036', 'fv_041', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_036_vins_fv041.pdf', 'APPROVED', true, '2025-11-03 11:00:00', 'ad_002', '2025-11-09 12:00:00'),
('fld_172', 'fl_036', 'fv_042', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_036_vreg_fv042.pdf', 'APPROVED', true, '2025-11-03 11:30:00', 'ad_002', '2025-11-09 12:30:00'),
('fld_173', 'fl_036', 'fv_042', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_036_vins_fv042.pdf', 'APPROVED', true, '2025-11-03 12:00:00', 'ad_002', '2025-11-09 13:00:00'),
('fld_174', 'fl_037', NULL, 'ID_CARD', 'https://example.com/docs/fl_037_id.pdf', 'APPROVED', true, '2025-11-07 09:00:00', 'ad_003', '2025-11-13 10:00:00'),
('fld_175', 'fl_037', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_037_dl.pdf', 'APPROVED', true, '2025-11-07 09:30:00', 'ad_003', '2025-11-13 10:30:00'),
('fld_176', 'fl_037', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_037_pdl.pdf', 'APPROVED', true, '2025-11-07 10:00:00', 'ad_003', '2025-11-13 11:00:00'),
('fld_177', 'fl_037', 'fv_043', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_037_vreg_fv043.pdf', 'APPROVED', true, '2025-11-07 10:30:00', 'ad_003', '2025-11-13 11:30:00'),
('fld_178', 'fl_037', 'fv_043', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_037_vins_fv043.pdf', 'APPROVED', true, '2025-11-07 11:00:00', 'ad_003', '2025-11-13 12:00:00'),
('fld_179', 'fl_038', NULL, 'ID_CARD', 'https://example.com/docs/fl_038_id.pdf', 'PENDING', true, '2025-11-12 09:00:00', NULL, NULL),
('fld_180', 'fl_038', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_038_dl.pdf', 'PENDING', true, '2025-11-12 09:30:00', NULL, NULL),
('fld_181', 'fl_038', 'fv_044', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_038_vreg_fv044.pdf', 'PENDING', true, '2025-11-12 10:00:00', NULL, NULL),
('fld_182', 'fl_038', 'fv_044', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_038_vins_fv044.pdf', 'PENDING', true, '2025-11-12 10:30:00', NULL, NULL),
('fld_183', 'fl_039', NULL, 'ID_CARD', 'https://example.com/docs/fl_039_id.pdf', 'APPROVED', true, '2025-11-17 09:00:00', 'ad_001', '2025-11-23 10:00:00'),
('fld_184', 'fl_039', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_039_dl.pdf', 'APPROVED', true, '2025-11-17 09:30:00', 'ad_001', '2025-11-23 10:30:00'),
('fld_185', 'fl_039', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_039_pdl.pdf', 'APPROVED', true, '2025-11-17 10:00:00', 'ad_001', '2025-11-23 11:00:00'),
('fld_186', 'fl_039', 'fv_045', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_039_vreg_fv045.pdf', 'APPROVED', true, '2025-11-17 10:30:00', 'ad_001', '2025-11-23 11:30:00'),
('fld_187', 'fl_039', 'fv_045', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_039_vins_fv045.pdf', 'APPROVED', true, '2025-11-17 11:00:00', 'ad_001', '2025-11-23 12:00:00'),
('fld_188', 'fl_040', NULL, 'ID_CARD', 'https://example.com/docs/fl_040_id.pdf', 'APPROVED', true, '2025-11-22 09:00:00', 'ad_002', '2025-11-28 10:00:00'),
('fld_189', 'fl_040', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_040_dl.pdf', 'APPROVED', true, '2025-11-22 09:30:00', 'ad_002', '2025-11-28 10:30:00'),
('fld_190', 'fl_040', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_040_pdl.pdf', 'APPROVED', true, '2025-11-22 10:00:00', 'ad_002', '2025-11-28 11:00:00'),
('fld_191', 'fl_040', 'fv_046', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_040_vreg_fv046.pdf', 'APPROVED', true, '2025-11-22 10:30:00', 'ad_002', '2025-11-28 11:30:00'),
('fld_192', 'fl_040', 'fv_046', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_040_vins_fv046.pdf', 'APPROVED', true, '2025-11-22 11:00:00', 'ad_002', '2025-11-28 12:00:00'),
('fld_193', 'fl_041', NULL, 'ID_CARD', 'https://example.com/docs/fl_041_id.pdf', 'REJECTED', true, '2025-12-03 09:00:00', 'ad_003', '2025-12-09 10:00:00'),
('fld_194', 'fl_041', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_041_dl.pdf', 'REJECTED', true, '2025-12-03 09:30:00', 'ad_003', '2025-12-09 10:30:00'),
('fld_195', 'fl_041', 'fv_047', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_041_vreg_fv047.pdf', 'REJECTED', true, '2025-12-03 10:00:00', 'ad_003', '2025-12-09 11:00:00'),
('fld_196', 'fl_041', 'fv_047', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_041_vins_fv047.pdf', 'REJECTED', true, '2025-12-03 10:30:00', 'ad_003', '2025-12-09 11:30:00'),
('fld_197', 'fl_042', NULL, 'ID_CARD', 'https://example.com/docs/fl_042_id.pdf', 'APPROVED', true, '2025-12-07 09:00:00', 'ad_001', '2025-12-13 10:00:00'),
('fld_198', 'fl_042', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_042_dl.pdf', 'APPROVED', true, '2025-12-07 09:30:00', 'ad_001', '2025-12-13 10:30:00'),
('fld_199', 'fl_042', 'fv_048', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_042_vreg_fv048.pdf', 'APPROVED', true, '2025-12-07 10:00:00', 'ad_001', '2025-12-13 11:00:00'),
('fld_200', 'fl_042', 'fv_048', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_042_vins_fv048.pdf', 'APPROVED', true, '2025-12-07 10:30:00', 'ad_001', '2025-12-13 11:30:00'),
('fld_201', 'fl_043', NULL, 'ID_CARD', 'https://example.com/docs/fl_043_id.pdf', 'PENDING', true, '2025-12-12 09:00:00', NULL, NULL),
('fld_202', 'fl_043', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_043_dl.pdf', 'PENDING', true, '2025-12-12 09:30:00', NULL, NULL),
('fld_203', 'fl_043', 'fv_049', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_043_vreg_fv049.pdf', 'PENDING', true, '2025-12-12 10:00:00', NULL, NULL),
('fld_204', 'fl_043', 'fv_049', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_043_vins_fv049.pdf', 'PENDING', true, '2025-12-12 10:30:00', NULL, NULL),
('fld_205', 'fl_044', NULL, 'ID_CARD', 'https://example.com/docs/fl_044_id.pdf', 'APPROVED', true, '2025-12-17 09:00:00', 'ad_002', '2025-12-23 10:00:00'),
('fld_206', 'fl_044', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_044_dl.pdf', 'APPROVED', true, '2025-12-17 09:30:00', 'ad_002', '2025-12-23 10:30:00'),
('fld_207', 'fl_044', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_044_pdl.pdf', 'APPROVED', true, '2025-12-17 10:00:00', 'ad_002', '2025-12-23 11:00:00'),
('fld_208', 'fl_044', 'fv_050', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_044_vreg_fv050.pdf', 'APPROVED', true, '2025-12-17 10:30:00', 'ad_002', '2025-12-23 11:30:00'),
('fld_209', 'fl_044', 'fv_050', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_044_vins_fv050.pdf', 'APPROVED', true, '2025-12-17 11:00:00', 'ad_002', '2025-12-23 12:00:00'),
('fld_210', 'fl_045', NULL, 'ID_CARD', 'https://example.com/docs/fl_045_id.pdf', 'APPROVED', true, '2025-12-22 09:00:00', 'ad_003', '2025-12-28 10:00:00'),
('fld_211', 'fl_045', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_045_dl.pdf', 'APPROVED', true, '2025-12-22 09:30:00', 'ad_003', '2025-12-28 10:30:00'),
('fld_212', 'fl_045', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_045_pdl.pdf', 'APPROVED', true, '2025-12-22 10:00:00', 'ad_003', '2025-12-28 11:00:00'),
('fld_213', 'fl_045', 'fv_051', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_045_vreg_fv051.pdf', 'APPROVED', true, '2025-12-22 10:30:00', 'ad_003', '2025-12-28 11:30:00'),
('fld_214', 'fl_045', 'fv_051', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_045_vins_fv051.pdf', 'APPROVED', true, '2025-12-22 11:00:00', 'ad_003', '2025-12-28 12:00:00'),
('fld_215', 'fl_046', NULL, 'ID_CARD', 'https://example.com/docs/fl_046_id.pdf', 'APPROVED', true, '2026-01-07 09:00:00', 'ad_001', '2026-01-13 10:00:00'),
('fld_216', 'fl_046', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_046_dl.pdf', 'APPROVED', true, '2026-01-07 09:30:00', 'ad_001', '2026-01-13 10:30:00'),
('fld_217', 'fl_046', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_046_pdl.pdf', 'APPROVED', true, '2026-01-07 10:00:00', 'ad_001', '2026-01-13 11:00:00'),
('fld_218', 'fl_046', 'fv_052', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_046_vreg_fv052.pdf', 'APPROVED', true, '2026-01-07 10:30:00', 'ad_001', '2026-01-13 11:30:00'),
('fld_219', 'fl_046', 'fv_052', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_046_vins_fv052.pdf', 'APPROVED', true, '2026-01-07 11:00:00', 'ad_001', '2026-01-13 12:00:00'),
('fld_220', 'fl_047', NULL, 'ID_CARD', 'https://example.com/docs/fl_047_id.pdf', 'REJECTED', true, '2026-01-12 09:00:00', 'ad_002', '2026-01-18 10:00:00'),
('fld_221', 'fl_047', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_047_dl.pdf', 'REJECTED', true, '2026-01-12 09:30:00', 'ad_002', '2026-01-18 10:30:00'),
('fld_222', 'fl_047', 'fv_053', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_047_vreg_fv053.pdf', 'REJECTED', true, '2026-01-12 10:00:00', 'ad_002', '2026-01-18 11:00:00'),
('fld_223', 'fl_047', 'fv_053', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_047_vins_fv053.pdf', 'REJECTED', true, '2026-01-12 10:30:00', 'ad_002', '2026-01-18 11:30:00'),
('fld_224', 'fl_048', NULL, 'ID_CARD', 'https://example.com/docs/fl_048_id.pdf', 'APPROVED', true, '2026-01-17 09:00:00', 'ad_003', '2026-01-23 10:00:00'),
('fld_225', 'fl_048', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_048_dl.pdf', 'APPROVED', true, '2026-01-17 09:30:00', 'ad_003', '2026-01-23 10:30:00'),
('fld_226', 'fl_048', 'fv_054', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_048_vreg_fv054.pdf', 'APPROVED', true, '2026-01-17 10:00:00', 'ad_003', '2026-01-23 11:00:00'),
('fld_227', 'fl_048', 'fv_054', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_048_vins_fv054.pdf', 'APPROVED', true, '2026-01-17 10:30:00', 'ad_003', '2026-01-23 11:30:00'),
('fld_228', 'fl_049', NULL, 'ID_CARD', 'https://example.com/docs/fl_049_id.pdf', 'PENDING', true, '2026-01-22 09:00:00', NULL, NULL),
('fld_229', 'fl_049', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_049_dl.pdf', 'PENDING', true, '2026-01-22 09:30:00', NULL, NULL),
('fld_230', 'fl_049', 'fv_055', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_049_vreg_fv055.pdf', 'PENDING', true, '2026-01-22 10:00:00', NULL, NULL),
('fld_231', 'fl_049', 'fv_055', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_049_vins_fv055.pdf', 'PENDING', true, '2026-01-22 10:30:00', NULL, NULL),
('fld_232', 'fl_050', NULL, 'ID_CARD', 'https://example.com/docs/fl_050_id.pdf', 'APPROVED', true, '2026-02-03 09:00:00', 'ad_001', '2026-02-09 10:00:00'),
('fld_233', 'fl_050', NULL, 'DRIVER_LICENSE', 'https://example.com/docs/fl_050_dl.pdf', 'APPROVED', true, '2026-02-03 09:30:00', 'ad_001', '2026-02-09 10:30:00'),
('fld_234', 'fl_050', NULL, 'PUBLIC_DRIVER_LICENSE', 'https://example.com/docs/fl_050_pdl.pdf', 'APPROVED', true, '2026-02-03 10:00:00', 'ad_001', '2026-02-09 11:00:00'),
('fld_235', 'fl_050', 'fv_056', 'VEHICLE_REGISTRATION', 'https://example.com/docs/fl_050_vreg_fv056.pdf', 'APPROVED', true, '2026-02-03 10:30:00', 'ad_001', '2026-02-09 11:30:00'),
('fld_236', 'fl_050', 'fv_056', 'VEHICLE_INSURANCE', 'https://example.com/docs/fl_050_vins_fv056.pdf', 'APPROVED', true, '2026-02-03 11:00:00', 'ad_001', '2026-02-09 12:00:00');

INSERT INTO fl_vehicle_images (fl_vehicle_image_id, fl_vehicle_id, fl_vehicle_image_url) VALUES
('fvi_001', 'fv_001', 'https://example.com/vehicles/fv_001_1.jpg'),
('fvi_002', 'fv_001', 'https://example.com/vehicles/fv_001_2.jpg'),
('fvi_003', 'fv_001', 'https://example.com/vehicles/fv_001_3.jpg'),
('fvi_004', 'fv_002', 'https://example.com/vehicles/fv_002_1.jpg'),
('fvi_005', 'fv_002', 'https://example.com/vehicles/fv_002_2.jpg'),
('fvi_006', 'fv_003', 'https://example.com/vehicles/fv_003_1.jpg'),
('fvi_007', 'fv_003', 'https://example.com/vehicles/fv_003_2.jpg'),
('fvi_008', 'fv_003', 'https://example.com/vehicles/fv_003_3.jpg'),
('fvi_009', 'fv_004', 'https://example.com/vehicles/fv_004_1.jpg'),
('fvi_010', 'fv_004', 'https://example.com/vehicles/fv_004_2.jpg'),
('fvi_011', 'fv_004', 'https://example.com/vehicles/fv_004_3.jpg'),
('fvi_012', 'fv_004', 'https://example.com/vehicles/fv_004_4.jpg'),
('fvi_013', 'fv_005', 'https://example.com/vehicles/fv_005_1.jpg'),
('fvi_014', 'fv_005', 'https://example.com/vehicles/fv_005_2.jpg'),
('fvi_015', 'fv_006', 'https://example.com/vehicles/fv_006_1.jpg'),
('fvi_016', 'fv_006', 'https://example.com/vehicles/fv_006_2.jpg'),
('fvi_017', 'fv_006', 'https://example.com/vehicles/fv_006_3.jpg'),
('fvi_018', 'fv_007', 'https://example.com/vehicles/fv_007_1.jpg'),
('fvi_019', 'fv_007', 'https://example.com/vehicles/fv_007_2.jpg'),
('fvi_020', 'fv_008', 'https://example.com/vehicles/fv_008_1.jpg'),
('fvi_021', 'fv_008', 'https://example.com/vehicles/fv_008_2.jpg'),
('fvi_022', 'fv_008', 'https://example.com/vehicles/fv_008_3.jpg'),
('fvi_023', 'fv_009', 'https://example.com/vehicles/fv_009_1.jpg'),
('fvi_024', 'fv_009', 'https://example.com/vehicles/fv_009_2.jpg'),
('fvi_025', 'fv_010', 'https://example.com/vehicles/fv_010_1.jpg'),
('fvi_026', 'fv_010', 'https://example.com/vehicles/fv_010_2.jpg'),
('fvi_027', 'fv_010', 'https://example.com/vehicles/fv_010_3.jpg'),
('fvi_028', 'fv_011', 'https://example.com/vehicles/fv_011_1.jpg'),
('fvi_029', 'fv_011', 'https://example.com/vehicles/fv_011_2.jpg'),
('fvi_030', 'fv_011', 'https://example.com/vehicles/fv_011_3.jpg'),
('fvi_031', 'fv_012', 'https://example.com/vehicles/fv_012_1.jpg'),
('fvi_032', 'fv_012', 'https://example.com/vehicles/fv_012_2.jpg'),
('fvi_033', 'fv_013', 'https://example.com/vehicles/fv_013_1.jpg'),
('fvi_034', 'fv_013', 'https://example.com/vehicles/fv_013_2.jpg'),
('fvi_035', 'fv_013', 'https://example.com/vehicles/fv_013_3.jpg'),
('fvi_036', 'fv_013', 'https://example.com/vehicles/fv_013_4.jpg'),
('fvi_037', 'fv_014', 'https://example.com/vehicles/fv_014_1.jpg'),
('fvi_038', 'fv_014', 'https://example.com/vehicles/fv_014_2.jpg'),
('fvi_039', 'fv_015', 'https://example.com/vehicles/fv_015_1.jpg'),
('fvi_040', 'fv_015', 'https://example.com/vehicles/fv_015_2.jpg'),
('fvi_041', 'fv_016', 'https://example.com/vehicles/fv_016_1.jpg'),
('fvi_042', 'fv_016', 'https://example.com/vehicles/fv_016_2.jpg'),
('fvi_043', 'fv_016', 'https://example.com/vehicles/fv_016_3.jpg'),
('fvi_044', 'fv_017', 'https://example.com/vehicles/fv_017_1.jpg'),
('fvi_045', 'fv_017', 'https://example.com/vehicles/fv_017_2.jpg'),
('fvi_046', 'fv_017', 'https://example.com/vehicles/fv_017_3.jpg'),
('fvi_047', 'fv_018', 'https://example.com/vehicles/fv_018_1.jpg'),
('fvi_048', 'fv_018', 'https://example.com/vehicles/fv_018_2.jpg'),
('fvi_049', 'fv_019', 'https://example.com/vehicles/fv_019_1.jpg'),
('fvi_050', 'fv_019', 'https://example.com/vehicles/fv_019_2.jpg'),
('fvi_051', 'fv_020', 'https://example.com/vehicles/fv_020_1.jpg'),
('fvi_052', 'fv_020', 'https://example.com/vehicles/fv_020_2.jpg'),
('fvi_053', 'fv_020', 'https://example.com/vehicles/fv_020_3.jpg'),
('fvi_054', 'fv_021', 'https://example.com/vehicles/fv_021_1.jpg'),
('fvi_055', 'fv_021', 'https://example.com/vehicles/fv_021_2.jpg'),
('fvi_056', 'fv_022', 'https://example.com/vehicles/fv_022_1.jpg'),
('fvi_057', 'fv_022', 'https://example.com/vehicles/fv_022_2.jpg'),
('fvi_058', 'fv_022', 'https://example.com/vehicles/fv_022_3.jpg'),
('fvi_059', 'fv_023', 'https://example.com/vehicles/fv_023_1.jpg'),
('fvi_060', 'fv_023', 'https://example.com/vehicles/fv_023_2.jpg'),
('fvi_061', 'fv_024', 'https://example.com/vehicles/fv_024_1.jpg'),
('fvi_062', 'fv_024', 'https://example.com/vehicles/fv_024_2.jpg'),
('fvi_063', 'fv_025', 'https://example.com/vehicles/fv_025_1.jpg'),
('fvi_064', 'fv_025', 'https://example.com/vehicles/fv_025_2.jpg'),
('fvi_065', 'fv_025', 'https://example.com/vehicles/fv_025_3.jpg'),
('fvi_066', 'fv_026', 'https://example.com/vehicles/fv_026_1.jpg'),
('fvi_067', 'fv_026', 'https://example.com/vehicles/fv_026_2.jpg'),
('fvi_068', 'fv_027', 'https://example.com/vehicles/fv_027_1.jpg'),
('fvi_069', 'fv_027', 'https://example.com/vehicles/fv_027_2.jpg'),
('fvi_070', 'fv_027', 'https://example.com/vehicles/fv_027_3.jpg'),
('fvi_071', 'fv_027', 'https://example.com/vehicles/fv_027_4.jpg'),
('fvi_072', 'fv_028', 'https://example.com/vehicles/fv_028_1.jpg'),
('fvi_073', 'fv_028', 'https://example.com/vehicles/fv_028_2.jpg'),
('fvi_074', 'fv_029', 'https://example.com/vehicles/fv_029_1.jpg'),
('fvi_075', 'fv_029', 'https://example.com/vehicles/fv_029_2.jpg'),
('fvi_076', 'fv_030', 'https://example.com/vehicles/fv_030_1.jpg'),
('fvi_077', 'fv_030', 'https://example.com/vehicles/fv_030_2.jpg'),
('fvi_078', 'fv_031', 'https://example.com/vehicles/fv_031_1.jpg'),
('fvi_079', 'fv_031', 'https://example.com/vehicles/fv_031_2.jpg'),
('fvi_080', 'fv_031', 'https://example.com/vehicles/fv_031_3.jpg'),
('fvi_081', 'fv_032', 'https://example.com/vehicles/fv_032_1.jpg'),
('fvi_082', 'fv_032', 'https://example.com/vehicles/fv_032_2.jpg'),
('fvi_083', 'fv_033', 'https://example.com/vehicles/fv_033_1.jpg'),
('fvi_084', 'fv_033', 'https://example.com/vehicles/fv_033_2.jpg'),
('fvi_085', 'fv_033', 'https://example.com/vehicles/fv_033_3.jpg'),
('fvi_086', 'fv_034', 'https://example.com/vehicles/fv_034_1.jpg'),
('fvi_087', 'fv_034', 'https://example.com/vehicles/fv_034_2.jpg'),
('fvi_088', 'fv_035', 'https://example.com/vehicles/fv_035_1.jpg'),
('fvi_089', 'fv_035', 'https://example.com/vehicles/fv_035_2.jpg'),
('fvi_090', 'fv_036', 'https://example.com/vehicles/fv_036_1.jpg'),
('fvi_091', 'fv_036', 'https://example.com/vehicles/fv_036_2.jpg'),
('fvi_092', 'fv_036', 'https://example.com/vehicles/fv_036_3.jpg'),
('fvi_093', 'fv_037', 'https://example.com/vehicles/fv_037_1.jpg'),
('fvi_094', 'fv_037', 'https://example.com/vehicles/fv_037_2.jpg'),
('fvi_095', 'fv_038', 'https://example.com/vehicles/fv_038_1.jpg'),
('fvi_096', 'fv_038', 'https://example.com/vehicles/fv_038_2.jpg'),
('fvi_097', 'fv_039', 'https://example.com/vehicles/fv_039_1.jpg'),
('fvi_098', 'fv_039', 'https://example.com/vehicles/fv_039_2.jpg'),
('fvi_099', 'fv_039', 'https://example.com/vehicles/fv_039_3.jpg'),
('fvi_100', 'fv_040', 'https://example.com/vehicles/fv_040_1.jpg'),
('fvi_101', 'fv_040', 'https://example.com/vehicles/fv_040_2.jpg'),
('fvi_102', 'fv_041', 'https://example.com/vehicles/fv_041_1.jpg'),
('fvi_103', 'fv_041', 'https://example.com/vehicles/fv_041_2.jpg'),
('fvi_104', 'fv_041', 'https://example.com/vehicles/fv_041_3.jpg'),
('fvi_105', 'fv_042', 'https://example.com/vehicles/fv_042_1.jpg'),
('fvi_106', 'fv_042', 'https://example.com/vehicles/fv_042_2.jpg'),
('fvi_107', 'fv_043', 'https://example.com/vehicles/fv_043_1.jpg'),
('fvi_108', 'fv_043', 'https://example.com/vehicles/fv_043_2.jpg'),
('fvi_109', 'fv_043', 'https://example.com/vehicles/fv_043_3.jpg'),
('fvi_110', 'fv_043', 'https://example.com/vehicles/fv_043_4.jpg'),
('fvi_111', 'fv_044', 'https://example.com/vehicles/fv_044_1.jpg'),
('fvi_112', 'fv_044', 'https://example.com/vehicles/fv_044_2.jpg'),
('fvi_113', 'fv_045', 'https://example.com/vehicles/fv_045_1.jpg'),
('fvi_114', 'fv_045', 'https://example.com/vehicles/fv_045_2.jpg'),
('fvi_115', 'fv_045', 'https://example.com/vehicles/fv_045_3.jpg'),
('fvi_116', 'fv_046', 'https://example.com/vehicles/fv_046_1.jpg'),
('fvi_117', 'fv_046', 'https://example.com/vehicles/fv_046_2.jpg'),
('fvi_118', 'fv_047', 'https://example.com/vehicles/fv_047_1.jpg'),
('fvi_119', 'fv_047', 'https://example.com/vehicles/fv_047_2.jpg'),
('fvi_120', 'fv_048', 'https://example.com/vehicles/fv_048_1.jpg'),
('fvi_121', 'fv_048', 'https://example.com/vehicles/fv_048_2.jpg'),
('fvi_122', 'fv_048', 'https://example.com/vehicles/fv_048_3.jpg'),
('fvi_123', 'fv_049', 'https://example.com/vehicles/fv_049_1.jpg'),
('fvi_124', 'fv_049', 'https://example.com/vehicles/fv_049_2.jpg'),
('fvi_125', 'fv_050', 'https://example.com/vehicles/fv_050_1.jpg'),
('fvi_126', 'fv_050', 'https://example.com/vehicles/fv_050_2.jpg'),
('fvi_127', 'fv_051', 'https://example.com/vehicles/fv_051_1.jpg'),
('fvi_128', 'fv_051', 'https://example.com/vehicles/fv_051_2.jpg'),
('fvi_129', 'fv_051', 'https://example.com/vehicles/fv_051_3.jpg'),
('fvi_130', 'fv_052', 'https://example.com/vehicles/fv_052_1.jpg'),
('fvi_131', 'fv_052', 'https://example.com/vehicles/fv_052_2.jpg'),
('fvi_132', 'fv_053', 'https://example.com/vehicles/fv_053_1.jpg'),
('fvi_133', 'fv_053', 'https://example.com/vehicles/fv_053_2.jpg'),
('fvi_134', 'fv_054', 'https://example.com/vehicles/fv_054_1.jpg'),
('fvi_135', 'fv_054', 'https://example.com/vehicles/fv_054_2.jpg'),
('fvi_136', 'fv_054', 'https://example.com/vehicles/fv_054_3.jpg'),
('fvi_137', 'fv_055', 'https://example.com/vehicles/fv_055_1.jpg'),
('fvi_138', 'fv_055', 'https://example.com/vehicles/fv_055_2.jpg'),
('fvi_139', 'fv_056', 'https://example.com/vehicles/fv_056_1.jpg'),
('fvi_140', 'fv_056', 'https://example.com/vehicles/fv_056_2.jpg'),
('fvi_141', 'fv_056', 'https://example.com/vehicles/fv_056_3.jpg'),
('fvi_142', 'fv_056', 'https://example.com/vehicles/fv_056_4.jpg');

INSERT INTO em_documents (em_doc_id, em_id, em_doc_type, file_url, em_doc_status, is_latest, em_uploaded_at, reviewed_by, reviewed_at) VALUES
('emd_001', 'em_001', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_001_reg_v1.pdf', 'REJECTED', false, '2025-01-20 10:00:00', 'ad_002', '2025-01-25 09:00:00'),
('emd_002', 'em_001', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_001_reg_v2.pdf', 'APPROVED', true, '2025-02-01 10:00:00', 'ad_002', '2025-02-05 10:00:00'),
('emd_003', 'em_001', 'TAX_ID', 'https://example.com/docs/em_001_tax.pdf', 'APPROVED', true, '2025-02-01 10:30:00', 'ad_002', '2025-02-05 10:30:00'),
('emd_004', 'em_002', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_002_reg.pdf', 'APPROVED', true, '2025-02-05 09:00:00', 'ad_003', '2025-02-10 11:00:00'),
('emd_005', 'em_002', 'TAX_ID', 'https://example.com/docs/em_002_tax.pdf', 'APPROVED', true, '2025-02-05 09:30:00', 'ad_003', '2025-02-10 11:30:00'),
('emd_006', 'em_003', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_003_reg.pdf', 'APPROVED', true, '2025-02-12 10:00:00', 'ad_001', '2025-02-18 09:00:00'),
('emd_007', 'em_003', 'TAX_ID', 'https://example.com/docs/em_003_tax.pdf', 'APPROVED', true, '2025-02-12 10:30:00', 'ad_001', '2025-02-18 09:30:00'),
('emd_008', 'em_004', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_004_reg.pdf', 'PENDING', true, '2025-03-10 11:00:00', NULL, NULL),
('emd_009', 'em_004', 'TAX_ID', 'https://example.com/docs/em_004_tax.pdf', 'PENDING', true, '2025-03-10 11:30:00', NULL, NULL),
('emd_010', 'em_005', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_005_reg.pdf', 'APPROVED', true, '2025-01-22 09:00:00', 'ad_002', '2025-01-28 10:00:00'),
('emd_011', 'em_005', 'TAX_ID', 'https://example.com/docs/em_005_tax.pdf', 'APPROVED', true, '2025-01-22 09:30:00', 'ad_002', '2025-01-28 10:30:00'),
('emd_012', 'em_006', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_006_reg.pdf', 'REJECTED', true, '2025-04-15 10:00:00', 'ad_003', '2025-04-20 09:00:00'),
('emd_013', 'em_007', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_007_reg.pdf', 'APPROVED', true, '2025-02-25 09:00:00', 'ad_001', '2025-03-02 10:00:00'),
('emd_014', 'em_007', 'TAX_ID', 'https://example.com/docs/em_007_tax.pdf', 'APPROVED', true, '2025-02-25 09:30:00', 'ad_001', '2025-03-02 10:30:00'),
('emd_015', 'em_008', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_008_reg.pdf', 'APPROVED', true, '2025-03-20 10:00:00', 'ad_002', '2025-03-26 09:00:00'),
('emd_016', 'em_008', 'TAX_ID', 'https://example.com/docs/em_008_tax.pdf', 'APPROVED', true, '2025-03-20 10:30:00', 'ad_002', '2025-03-26 09:30:00'),
('emd_017', 'em_009', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_009_reg.pdf', 'PENDING', true, '2025-04-05 09:00:00', NULL, NULL),
('emd_018', 'em_010', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_010_reg.pdf', 'REJECTED', true, '2025-05-10 10:00:00', 'ad_003', '2025-05-15 09:00:00'),
('emd_019', 'em_011', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_011_reg.pdf', 'APPROVED', true, '2025-03-28 09:00:00', 'ad_001', '2025-04-03 10:00:00'),
('emd_020', 'em_011', 'TAX_ID', 'https://example.com/docs/em_011_tax.pdf', 'APPROVED', true, '2025-03-28 09:30:00', 'ad_001', '2025-04-03 10:30:00'),
('emd_021', 'em_012', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_012_reg.pdf', 'APPROVED', true, '2025-02-18 09:00:00', 'ad_002', '2025-02-24 10:00:00'),
('emd_022', 'em_012', 'TAX_ID', 'https://example.com/docs/em_012_tax.pdf', 'APPROVED', true, '2025-02-18 09:30:00', 'ad_002', '2025-02-24 10:30:00'),
('emd_023', 'em_013', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_013_reg.pdf', 'PENDING', true, '2025-06-05 10:00:00', NULL, NULL),
('emd_024', 'em_014', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_014_reg.pdf', 'APPROVED', true, '2025-02-01 09:00:00', 'ad_003', '2025-02-07 10:00:00'),
('emd_025', 'em_014', 'TAX_ID', 'https://example.com/docs/em_014_tax.pdf', 'APPROVED', true, '2025-02-01 09:30:00', 'ad_003', '2025-02-07 10:30:00'),
('emd_026', 'em_015', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_015_reg.pdf', 'APPROVED', true, '2025-04-22 09:00:00', 'ad_001', '2025-04-28 10:00:00'),
('emd_027', 'em_015', 'TAX_ID', 'https://example.com/docs/em_015_tax.pdf', 'APPROVED', true, '2025-04-22 09:30:00', 'ad_001', '2025-04-28 10:30:00'),
('emd_028', 'em_016', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_016_reg.pdf', 'REJECTED', true, '2025-07-12 10:00:00', 'ad_002', '2025-07-18 09:00:00'),
('emd_029', 'em_017', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_017_reg.pdf', 'APPROVED', true, '2025-02-10 09:00:00', 'ad_003', '2025-02-16 10:00:00'),
('emd_030', 'em_017', 'TAX_ID', 'https://example.com/docs/em_017_tax.pdf', 'APPROVED', true, '2025-02-10 09:30:00', 'ad_003', '2025-02-16 10:30:00'),
('emd_031', 'em_018', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_018_reg.pdf', 'PENDING', true, '2025-05-18 10:00:00', NULL, NULL),
('emd_032', 'em_019', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_019_reg.pdf', 'APPROVED', true, '2025-04-02 09:00:00', 'ad_001', '2025-04-08 10:00:00'),
('emd_033', 'em_019', 'TAX_ID', 'https://example.com/docs/em_019_tax.pdf', 'APPROVED', true, '2025-04-02 09:30:00', 'ad_001', '2025-04-08 10:30:00'),
('emd_034', 'em_020', 'COMPANY_REGISTRATION', 'https://example.com/docs/em_020_reg.pdf', 'REJECTED', true, '2025-08-05 10:00:00', 'ad_002', '2025-08-10 09:00:00');

INSERT INTO em_verification (em_verify_id, em_id, em_verify_status, em_submitted_at, em_verified_at, reviewed_by) VALUES
('emv_001', 'em_001', 'VERIFIED', '2025-01-20 10:00:00', '2025-02-05 10:00:00', 'ad_002'),
('emv_002', 'em_002', 'VERIFIED', '2025-02-05 09:00:00', '2025-02-10 11:00:00', 'ad_003'),
('emv_003', 'em_003', 'VERIFIED', '2025-02-12 10:00:00', '2025-02-18 09:00:00', 'ad_001'),
('emv_004', 'em_004', 'PENDING', '2025-03-10 11:00:00', NULL, NULL),
('emv_005', 'em_005', 'VERIFIED', '2025-01-22 09:00:00', '2025-01-28 10:00:00', 'ad_002'),
('emv_006', 'em_006', 'NOT_VERIFIED', '2025-04-15 10:00:00', NULL, NULL),
('emv_007', 'em_007', 'VERIFIED', '2025-02-25 09:00:00', '2025-03-02 10:00:00', 'ad_001'),
('emv_008', 'em_008', 'VERIFIED', '2025-03-20 10:00:00', '2025-03-26 09:00:00', 'ad_002'),
('emv_009', 'em_009', 'PENDING', '2025-04-05 09:00:00', NULL, NULL),
('emv_010', 'em_010', 'NOT_VERIFIED', '2025-05-10 10:00:00', NULL, NULL),
('emv_011', 'em_011', 'VERIFIED', '2025-03-28 09:00:00', '2025-04-03 10:00:00', 'ad_001'),
('emv_012', 'em_012', 'VERIFIED', '2025-02-18 09:00:00', '2025-02-24 10:00:00', 'ad_002'),
('emv_013', 'em_013', 'PENDING', '2025-06-05 10:00:00', NULL, NULL),
('emv_014', 'em_014', 'VERIFIED', '2025-02-01 09:00:00', '2025-02-07 10:00:00', 'ad_003'),
('emv_015', 'em_015', 'VERIFIED', '2025-04-22 09:00:00', '2025-04-28 10:00:00', 'ad_001'),
('emv_016', 'em_016', 'NOT_VERIFIED', '2025-07-12 10:00:00', NULL, NULL),
('emv_017', 'em_017', 'VERIFIED', '2025-02-10 09:00:00', '2025-02-16 10:00:00', 'ad_003'),
('emv_018', 'em_018', 'PENDING', '2025-05-18 10:00:00', NULL, NULL),
('emv_019', 'em_019', 'VERIFIED', '2025-04-02 09:00:00', '2025-04-08 10:00:00', 'ad_001'),
('emv_020', 'em_020', 'NOT_VERIFIED', '2025-08-05 10:00:00', NULL, NULL);

INSERT INTO fl_verification (fl_verify_id, fl_id, fl_verify_status, fl_submitted_at, fl_verified_at, reviewed_by) VALUES
('flv_001', 'fl_001', 'VERIFIED', '2025-01-22 09:00:00', '2025-01-28 10:00:00', 'ad_001'),
('flv_002', 'fl_002', 'VERIFIED', '2025-01-27 09:00:00', '2025-02-02 10:00:00', 'ad_002'),
('flv_003', 'fl_003', 'VERIFIED', '2025-02-03 09:00:00', '2025-02-09 10:00:00', 'ad_003'),
('flv_004', 'fl_004', 'PENDING', '2025-02-12 09:00:00', NULL, NULL),
('flv_005', 'fl_005', 'VERIFIED', '2025-02-17 09:00:00', '2025-02-23 10:00:00', 'ad_001'),
('flv_006', 'fl_006', 'VERIFIED', '2025-03-03 09:00:00', '2025-03-09 10:00:00', 'ad_002'),
('flv_007', 'fl_007', 'NOT_VERIFIED', '2025-03-12 09:00:00', NULL, NULL),
('flv_008', 'fl_008', 'VERIFIED', '2025-03-17 09:00:00', '2025-03-23 10:00:00', 'ad_001'),
('flv_009', 'fl_009', 'VERIFIED', '2025-04-03 09:00:00', '2025-04-09 10:00:00', 'ad_002'),
('flv_010', 'fl_010', 'PENDING', '2025-04-12 09:00:00', NULL, NULL),
('flv_011', 'fl_011', 'VERIFIED', '2025-01-12 09:00:00', '2025-01-18 10:00:00', 'ad_003'),
('flv_012', 'fl_012', 'VERIFIED', '2025-04-22 09:00:00', '2025-04-28 10:00:00', 'ad_001'),
('flv_013', 'fl_013', 'NOT_VERIFIED', '2025-05-03 09:00:00', NULL, NULL),
('flv_014', 'fl_014', 'VERIFIED', '2025-05-12 09:00:00', '2025-05-18 10:00:00', 'ad_003'),
('flv_015', 'fl_015', 'PENDING', '2025-05-22 09:00:00', NULL, NULL),
('flv_016', 'fl_016', 'VERIFIED', '2025-06-03 09:00:00', '2025-06-09 10:00:00', 'ad_001'),
('flv_017', 'fl_017', 'VERIFIED', '2025-06-12 09:00:00', '2025-06-18 10:00:00', 'ad_002'),
('flv_018', 'fl_018', 'NOT_VERIFIED', '2025-06-22 09:00:00', NULL, NULL),
('flv_019', 'fl_019', 'VERIFIED', '2025-07-03 09:00:00', '2025-07-09 10:00:00', 'ad_001'),
('flv_020', 'fl_020', 'PENDING', '2025-07-12 09:00:00', NULL, NULL),
('flv_021', 'fl_021', 'VERIFIED', '2025-07-17 09:00:00', '2025-07-23 10:00:00', 'ad_002'),
('flv_022', 'fl_022', 'VERIFIED', '2025-07-22 09:00:00', '2025-07-28 10:00:00', 'ad_003'),
('flv_023', 'fl_023', 'VERIFIED', '2025-08-03 09:00:00', '2025-08-09 10:00:00', 'ad_001'),
('flv_024', 'fl_024', 'PENDING', '2025-08-12 09:00:00', NULL, NULL),
('flv_025', 'fl_025', 'NOT_VERIFIED', '2025-08-17 09:00:00', NULL, NULL),
('flv_026', 'fl_026', 'VERIFIED', '2025-08-22 09:00:00', '2025-08-28 10:00:00', 'ad_003'),
('flv_027', 'fl_027', 'VERIFIED', '2025-09-03 09:00:00', '2025-09-09 10:00:00', 'ad_001'),
('flv_028', 'fl_028', 'VERIFIED', '2025-09-07 09:00:00', '2025-09-13 10:00:00', 'ad_002'),
('flv_029', 'fl_029', 'NOT_VERIFIED', '2025-09-12 09:00:00', NULL, NULL),
('flv_030', 'fl_030', 'PENDING', '2025-09-17 09:00:00', NULL, NULL),
('flv_031', 'fl_031', 'VERIFIED', '2025-09-22 09:00:00', '2025-09-28 10:00:00', 'ad_001'),
('flv_032', 'fl_032', 'VERIFIED', '2025-10-03 09:00:00', '2025-10-09 10:00:00', 'ad_002'),
('flv_033', 'fl_033', 'PENDING', '2025-10-10 09:00:00', NULL, NULL),
('flv_034', 'fl_034', 'VERIFIED', '2025-10-17 09:00:00', '2025-10-23 10:00:00', 'ad_003'),
('flv_035', 'fl_035', 'NOT_VERIFIED', '2025-10-22 09:00:00', NULL, NULL),
('flv_036', 'fl_036', 'VERIFIED', '2025-11-03 09:00:00', '2025-11-09 10:00:00', 'ad_002'),
('flv_037', 'fl_037', 'VERIFIED', '2025-11-07 09:00:00', '2025-11-13 10:00:00', 'ad_003'),
('flv_038', 'fl_038', 'PENDING', '2025-11-12 09:00:00', NULL, NULL),
('flv_039', 'fl_039', 'VERIFIED', '2025-11-17 09:00:00', '2025-11-23 10:00:00', 'ad_001'),
('flv_040', 'fl_040', 'VERIFIED', '2025-11-22 09:00:00', '2025-11-28 10:00:00', 'ad_002'),
('flv_041', 'fl_041', 'NOT_VERIFIED', '2025-12-03 09:00:00', NULL, NULL),
('flv_042', 'fl_042', 'VERIFIED', '2025-12-07 09:00:00', '2025-12-13 10:00:00', 'ad_001'),
('flv_043', 'fl_043', 'PENDING', '2025-12-12 09:00:00', NULL, NULL),
('flv_044', 'fl_044', 'VERIFIED', '2025-12-17 09:00:00', '2025-12-23 10:00:00', 'ad_002'),
('flv_045', 'fl_045', 'VERIFIED', '2025-12-22 09:00:00', '2025-12-28 10:00:00', 'ad_003'),
('flv_046', 'fl_046', 'VERIFIED', '2026-01-07 09:00:00', '2026-01-13 10:00:00', 'ad_001'),
('flv_047', 'fl_047', 'NOT_VERIFIED', '2026-01-12 09:00:00', NULL, NULL),
('flv_048', 'fl_048', 'VERIFIED', '2026-01-17 09:00:00', '2026-01-23 10:00:00', 'ad_003'),
('flv_049', 'fl_049', 'PENDING', '2026-01-22 09:00:00', NULL, NULL),
('flv_050', 'fl_050', 'VERIFIED', '2026-02-03 09:00:00', '2026-02-09 10:00:00', 'ad_001');

INSERT INTO admin_logs (log_id, admin_id, action, created_at) VALUES
('log_001', 'ad_001', 'approve_document:fld_001', '2025-01-28 10:00:00'),
('log_002', 'ad_001', 'approve_document:fld_002', '2025-01-28 10:30:00'),
('log_003', 'ad_001', 'approve_document:fld_003', '2025-01-28 11:00:00'),
('log_004', 'ad_001', 'approve_document:fld_004', '2025-01-28 11:30:00'),
('log_005', 'ad_001', 'approve_document:fld_005', '2025-01-28 12:00:00'),
('log_006', 'ad_001', 'verify_user:fl_001', '2025-01-28 12:30:00'),
('log_007', 'ad_002', 'approve_document:emd_002', '2025-02-05 10:00:00'),
('log_008', 'ad_002', 'approve_document:emd_003', '2025-02-05 10:30:00'),
('log_009', 'ad_002', 'verify_employer:em_001', '2025-02-05 11:00:00'),
('log_010', 'ad_002', 'approve_document:fld_008', '2025-02-02 10:00:00'),
('log_011', 'ad_002', 'approve_document:fld_009', '2025-02-02 10:30:00'),
('log_012', 'ad_002', 'verify_user:fl_002', '2025-02-02 11:00:00'),
('log_013', 'ad_003', 'approve_document:emd_004', '2025-02-10 11:00:00'),
('log_014', 'ad_003', 'verify_employer:em_002', '2025-02-10 11:30:00'),
('log_015', 'ad_003', 'approve_document:fld_013', '2025-02-09 10:00:00'),
('log_016', 'ad_003', 'approve_document:fld_014', '2025-02-09 10:30:00'),
('log_017', 'ad_003', 'verify_user:fl_003', '2025-02-09 11:00:00'),
('log_018', 'ad_001', 'approve_document:emd_006', '2025-02-18 09:00:00'),
('log_019', 'ad_001', 'verify_employer:em_003', '2025-02-18 09:30:00'),
('log_020', 'ad_001', 'approve_document:fld_022', '2025-02-23 10:00:00'),
('log_021', 'ad_001', 'verify_user:fl_005', '2025-02-23 11:00:00'),
('log_022', 'ad_002', 'reject_document:emd_001', '2025-01-25 09:00:00'),
('log_023', 'ad_002', 'approve_document:emd_010', '2025-01-28 10:00:00'),
('log_024', 'ad_002', 'verify_employer:em_005', '2025-01-28 11:00:00'),
('log_025', 'ad_003', 'reject_document:fld_032', '2025-03-18 10:00:00'),
('log_026', 'ad_003', 'reject_document:fld_033', '2025-04-07 10:00:00'),
('log_027', 'ad_003', 'reject_document:fld_034', '2025-03-18 10:30:00'),
('log_028', 'ad_003', 'reject_user:fl_007', '2025-04-07 11:00:00'),
('log_029', 'ad_001', 'approve_document:fld_037', '2025-03-23 10:00:00'),
('log_030', 'ad_001', 'approve_document:fld_038', '2025-03-23 10:30:00'),
('log_031', 'ad_001', 'verify_user:fl_008', '2025-03-23 11:00:00'),
('log_032', 'ad_002', 'approve_document:fld_042', '2025-04-09 10:00:00'),
('log_033', 'ad_002', 'verify_user:fl_009', '2025-04-09 11:00:00'),
('log_034', 'ad_003', 'approve_document:emd_013', '2025-03-02 10:00:00'),
('log_035', 'ad_003', 'verify_employer:em_007', '2025-03-02 11:00:00'),
('log_036', 'ad_002', 'approve_document:emd_015', '2025-03-26 09:00:00'),
('log_037', 'ad_002', 'verify_employer:em_008', '2025-03-26 10:00:00'),
('log_038', 'ad_003', 'reject_document:emd_012', '2025-04-20 09:00:00'),
('log_039', 'ad_003', 'reject_employer:em_006', '2025-04-20 09:30:00'),
('log_040', 'ad_001', 'approve_document:fld_027', '2025-03-09 10:00:00'),
('log_041', 'ad_001', 'verify_user:fl_006', '2025-03-09 11:00:00'),
('log_042', 'ad_001', 'approve_document:fld_051', '2025-01-18 10:00:00'),
('log_043', 'ad_001', 'verify_user:fl_011', '2025-01-18 11:00:00'),
('log_044', 'ad_002', 'reject_document:fld_062', '2025-05-09 10:00:00'),
('log_045', 'ad_002', 'reject_user:fl_013', '2025-05-09 11:00:00'),
('log_046', 'ad_003', 'approve_document:fld_066', '2025-05-18 10:00:00'),
('log_047', 'ad_003', 'verify_user:fl_014', '2025-05-18 11:00:00'),
('log_048', 'ad_001', 'approve_document:emd_019', '2025-04-03 10:00:00'),
('log_049', 'ad_001', 'verify_employer:em_011', '2025-04-03 11:00:00'),
('log_050', 'ad_002', 'approve_document:emd_021', '2025-02-24 10:00:00'),
('log_051', 'ad_002', 'verify_employer:em_012', '2025-02-24 11:00:00'),
('log_052', 'ad_001', 'approve_document:fld_075', '2025-06-09 10:00:00'),
('log_053', 'ad_001', 'verify_user:fl_016', '2025-06-09 11:00:00'),
('log_054', 'ad_002', 'approve_document:fld_080', '2025-06-18 10:00:00'),
('log_055', 'ad_002', 'verify_user:fl_017', '2025-06-18 11:00:00'),
('log_056', 'ad_003', 'reject_document:fld_085', '2025-06-28 10:00:00'),
('log_057', 'ad_003', 'reject_user:fl_018', '2025-06-28 11:00:00'),
('log_058', 'ad_003', 'reject_document:emd_018', '2025-07-18 09:00:00'),
('log_059', 'ad_001', 'approve_document:fld_089', '2025-07-09 10:00:00'),
('log_060', 'ad_001', 'verify_user:fl_019', '2025-07-09 11:00:00'),
('log_061', 'ad_002', 'approve_document:fld_098', '2025-07-23 10:00:00'),
('log_062', 'ad_002', 'verify_user:fl_021', '2025-07-23 11:00:00'),
('log_063', 'ad_003', 'approve_document:fld_103', '2025-07-28 10:00:00'),
('log_064', 'ad_003', 'verify_user:fl_022', '2025-07-28 11:00:00'),
('log_065', 'ad_001', 'approve_document:fld_107', '2025-08-09 10:00:00'),
('log_066', 'ad_001', 'verify_user:fl_023', '2025-08-09 11:00:00'),
('log_067', 'ad_002', 'reject_document:fld_118', '2025-08-23 10:00:00'),
('log_068', 'ad_002', 'reject_user:fl_025', '2025-08-23 11:00:00'),
('log_069', 'ad_003', 'approve_document:fld_122', '2025-08-28 10:00:00'),
('log_070', 'ad_003', 'verify_user:fl_026', '2025-08-28 11:00:00'),
('log_071', 'ad_001', 'approve_document:fld_127', '2025-09-09 10:00:00'),
('log_072', 'ad_001', 'verify_user:fl_027', '2025-09-09 11:00:00'),
('log_073', 'ad_002', 'approve_document:fld_132', '2025-09-13 10:00:00'),
('log_074', 'ad_002', 'verify_user:fl_028', '2025-09-13 11:00:00'),
('log_075', 'ad_003', 'reject_document:fld_137', '2025-09-18 10:00:00'),
('log_076', 'ad_003', 'reject_user:fl_029', '2025-09-18 11:00:00'),
('log_077', 'ad_001', 'approve_document:fld_145', '2025-09-28 10:00:00'),
('log_078', 'ad_001', 'verify_user:fl_031', '2025-09-28 11:00:00'),
('log_079', 'ad_002', 'approve_document:fld_150', '2025-10-09 10:00:00'),
('log_080', 'ad_002', 'verify_user:fl_032', '2025-10-09 11:00:00'),
('log_081', 'ad_003', 'approve_document:fld_158', '2025-10-23 10:00:00'),
('log_082', 'ad_003', 'verify_user:fl_034', '2025-10-23 11:00:00'),
('log_083', 'ad_001', 'reject_document:fld_163', '2025-10-28 10:00:00'),
('log_084', 'ad_001', 'reject_user:fl_035', '2025-10-28 11:00:00'),
('log_085', 'ad_002', 'approve_document:fld_167', '2025-11-09 10:00:00'),
('log_086', 'ad_002', 'verify_user:fl_036', '2025-11-09 11:00:00'),
('log_087', 'ad_003', 'approve_document:fld_174', '2025-11-13 10:00:00'),
('log_088', 'ad_003', 'verify_user:fl_037', '2025-11-13 11:00:00'),
('log_089', 'ad_001', 'approve_document:fld_183', '2025-11-23 10:00:00'),
('log_090', 'ad_001', 'verify_user:fl_039', '2025-11-23 11:00:00'),
('log_091', 'ad_002', 'approve_document:fld_188', '2025-11-28 10:00:00'),
('log_092', 'ad_002', 'verify_user:fl_040', '2025-11-28 11:00:00'),
('log_093', 'ad_003', 'reject_document:fld_193', '2025-12-09 10:00:00'),
('log_094', 'ad_003', 'reject_user:fl_041', '2025-12-09 11:00:00'),
('log_095', 'ad_001', 'approve_document:fld_197', '2025-12-13 10:00:00'),
('log_096', 'ad_001', 'verify_user:fl_042', '2025-12-13 11:00:00'),
('log_097', 'ad_002', 'approve_document:fld_205', '2025-12-23 10:00:00'),
('log_098', 'ad_002', 'verify_user:fl_044', '2025-12-23 11:00:00'),
('log_099', 'ad_003', 'approve_document:fld_210', '2025-12-28 10:00:00'),
('log_100', 'ad_003', 'verify_user:fl_045', '2025-12-28 11:00:00'),
('log_101', 'ad_001', 'approve_document:fld_215', '2026-01-13 10:00:00'),
('log_102', 'ad_001', 'verify_user:fl_046', '2026-01-13 11:00:00'),
('log_103', 'ad_002', 'reject_document:fld_220', '2026-01-18 10:00:00'),
('log_104', 'ad_002', 'reject_user:fl_047', '2026-01-18 11:00:00'),
('log_105', 'ad_003', 'approve_document:fld_224', '2026-01-23 10:00:00'),
('log_106', 'ad_003', 'verify_user:fl_048', '2026-01-23 11:00:00'),
('log_107', 'ad_001', 'approve_document:fld_232', '2026-02-09 10:00:00'),
('log_108', 'ad_001', 'verify_user:fl_050', '2026-02-09 11:00:00'),
('log_109', 'ad_001', 'approve_document:fld_058', '2025-04-28 10:00:00'),
('log_110', 'ad_001', 'verify_user:fl_012', '2025-04-28 11:00:00'),
('log_111', 'ad_003', 'approve_document:emd_024', '2025-02-07 10:00:00'),
('log_112', 'ad_003', 'verify_employer:em_014', '2025-02-07 11:00:00'),
('log_113', 'ad_001', 'approve_document:emd_026', '2025-04-28 10:00:00'),
('log_114', 'ad_001', 'verify_employer:em_015', '2025-04-28 11:00:00'),
('log_115', 'ad_003', 'approve_document:emd_029', '2025-02-16 10:00:00'),
('log_116', 'ad_003', 'verify_employer:em_017', '2025-02-16 11:00:00'),
('log_117', 'ad_001', 'approve_document:emd_032', '2025-04-08 10:00:00'),
('log_118', 'ad_001', 'verify_employer:em_019', '2025-04-08 11:00:00'),
('log_119', 'ad_002', 'reject_document:emd_028', '2025-07-18 09:00:00'),
('log_120', 'ad_002', 'reject_document:emd_034', '2025-08-10 09:00:00');


INSERT INTO jobs (job_id, em_id, job_title, job_description, job_start_date, job_end_date, job_required_vehicle_type, job_required_seat, job_price, job_status, selected_fl_id, job_created_at, job_updated_at) VALUES
('job_001','em_002','Chiang Mai Old City & Doi Suthep Full Day','[Chiang Mai Old City & Doi Suthep Full Day]
Driver: Mr. Wanchai / 0812001001
Guide: Ms. Nattaya / 0891002002
Tour Schedule:
07:00-07:30 Hotel pick up
08:30-10:00 Doi Suthep Temple
10:30-12:00 Old City Moat Walk
12:00-13:00 Lanna Lunch Restaurant
13:30-15:00 Silver Handicraft Workshop San Kamphaeng
15:30-17:00 Elephant Nature Park Observation
17:30-18:00 Night Bazaar Drop Off
Including:
- Toyota Commuter VAN
- English & Mandarin Guide
- Bottled water and snacks
- All entrance fees
Not Included:
- Personal expenses
Remark:
Schedule may change depending on local conditions.','2026-05-10','2026-05-10','VAN',10,4500.00,'COMPLETED','fl_001','2026-04-01 09:00:00','2026-05-11 08:00:00'),
('job_002','em_003','Phuket Old Town & Big Buddha VIP Tour','[Phuket Old Town & Big Buddha VIP Tour]
Driver: Mr. Krit / 0813002002
Guide: Mr. Apirak / 0892003003
Tour Schedule:
08:00-08:30 Hotel pick up
09:30-10:30 Wat Chalong Temple
10:45-11:45 Phuket Big Buddha
12:30-14:00 Phuket Old Town Walking Tour
15:30-16:30 Promthep Cape Viewpoint
17:00-17:45 Rawai Seafood Market
18:30-19:00 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- Bottled water and fruit
- Entrance fees included
Not Included:
- Seafood purchases at Rawai
Remark:
Promthep Cape timing may shift to catch the best sunset light.','2026-05-15','2026-05-15','VAN',9,7200.00,'COMPLETED','fl_003','2026-04-05 10:00:00','2026-05-16 09:00:00'),
('job_003','em_015','Krabi 4-Island Speedboat & Snorkeling Tour','[Krabi 4-Island Speedboat & Snorkeling Tour]
Driver: Mr. Chalee / 0814003003
Guide: Ms. Supaporn / 0893004004
Tour Schedule:
07:30-08:00 Hotel pick up
08:30-09:00 Departure from Nopparat Thara Pier
09:30-10:45 Poda Island Snorkeling
11:00-11:30 Chicken Island Photo Stop
12:00-13:00 Tub Island Beach Lunch
13:30-14:30 Mor Krabi Cave Exploration
15:00-15:45 Princess Cave Pranang
16:30-17:00 Return & Hotel Drop Off
Including:
- Hyundai H1 VAN transfer
- English Guide
- Snorkeling equipment
- Lunch on beach
Not Included:
- Personal beverages
Remark:
Tour may be cancelled due to sea conditions.','2026-05-20','2026-05-20','VAN',9,5800.00,'COMPLETED','fl_016','2026-04-08 11:00:00','2026-05-21 09:00:00'),
('job_004','em_004','Chiang Rai White Temple & Golden Triangle Tour','[Chiang Rai White Temple & Golden Triangle Tour]
Driver: Mr. Somchai / 0815004004
Guide: Mr. Anan / 0894005005
Tour Schedule:
07:00-07:30 Hotel pick up
08:00-09:30 Wat Rong Khun White Temple
10:00-11:00 Baan Dam Museum Black House
12:00-13:00 Riverside Lunch
13:30-15:00 Golden Triangle & Hall of Opium
15:30-16:45 Doi Tung Royal Villa and Garden
17:30-18:30 Mae Sai Border Town Shopping
19:00-19:30 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- Water and snacks
- All entrance fees
Not Included:
- Personal shopping
Remark:
Schedule may change depending on road conditions.','2026-05-22','2026-05-22','VAN',10,8500.00,'COMPLETED','fl_045','2026-04-10 09:00:00','2026-05-23 10:00:00'),
('job_005','em_011','Pattaya City Tour & Nong Nooch Garden','[Pattaya City Tour & Nong Nooch Garden]
Driver: Mr. Preecha / 0816005005
Guide: Ms. Kanokwan / 0895006006
Tour Schedule:
08:00-08:30 Hotel pick up
09:00-10:30 Sanctuary of Truth
10:45-11:30 Viewpoint Hill Khao Phra Tamnak
12:00-13:15 Lunch at Walking Street Area
13:30-15:15 Nong Nooch Tropical Garden
15:30-16:30 Nong Nooch Cultural Show
17:00-18:15 Pattaya Floating Market
18:30-19:00 Hotel drop off
Including:
- Hyundai H1 VAN
- English Guide
- Entrance to Nong Nooch
- Water and snacks
Not Included:
- Lunch cost
Remark:
Cultural show is fixed at 15:30. Please be on time.','2026-06-01','2026-06-01','VAN',9,5200.00,'COMPLETED','fl_017','2026-04-15 10:00:00','2026-06-02 08:00:00'),
('job_006','em_019','Chonburi Tiger Zoo & Bang Saen Beach Tour','[Chonburi Tiger Zoo & Bang Saen Beach Tour]
Driver: Mr. Thanat / 0817006006
Guide: Ms. Pensri / 0896007007
Tour Schedule:
07:30-08:00 Hotel pick up
08:30-10:15 Sriracha Tiger Zoo
10:30-11:15 Crocodile Show
12:00-13:15 Ko Loi Seafood Lunch
14:30-16:15 Bang Saen Beach Leisure
16:30-17:45 Wat Saman Rattanaram Giant Ganesh
18:30-19:00 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- Tiger Zoo entrance
- Bottled water
Not Included:
- Lunch
Remark:
Allow extra time on weekends.','2026-06-05','2026-06-05','VAN',10,4800.00,'COMPLETED','fl_028','2026-04-18 08:00:00','2026-06-06 08:00:00'),
('job_007','em_002','Doi Inthanon National Park & Waterfalls Tour','[Doi Inthanon National Park & Waterfalls Tour]
Driver: Mr. Yutthana / 0818007007
Guide: Mr. Rungrot / 0897008008
Tour Schedule:
06:30-07:00 Hotel pick up
08:30-09:30 Wachirathan Waterfall
10:00-11:00 Twin Royal Pagodas
11:30-12:15 Summit of Doi Inthanon
13:00-14:00 Lunch at Royal Agricultural Research Center
14:30-15:15 Sirithan Waterfall
16:00-17:15 Karen Hill Tribe Village
18:00-18:30 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- National park entrance fees
- Water and snacks
Not Included:
- Personal purchases at village
Remark:
Summit can be cold 12-18 degrees. Bring a light jacket.','2026-06-08','2026-06-08','VAN',10,5500.00,'SELECTED','fl_001','2026-04-20 09:00:00','2026-05-02 13:00:00'),
('job_008','em_015','Krabi Kayaking & Mangrove Eco Tour','[Krabi Kayaking & Mangrove Eco Tour]
Driver: Mr. Niphon / 0819008008
Guide: Ms. Duangjai / 0898009009
Tour Schedule:
08:00-08:30 Hotel pick up
09:00-09:30 Ao Thalane Kayak Briefing
09:30-11:30 Mangrove Forest Kayaking
11:30-12:15 Bat Cave Exploration
12:30-13:30 Sandbar Picnic Lunch
14:00-15:15 Lagoon Return Paddle
15:30-17:30 Tiger Cave Temple Climb
18:30-19:00 Hotel drop off
Including:
- Hyundai H1 VAN transfer
- English Guide
- Kayak equipment
- Picnic lunch
Not Included:
- Personal expenses
Remark:
Guests should be in reasonable physical condition.','2026-06-12','2026-06-12','VAN',9,4900.00,'SELECTED','fl_036','2026-04-22 11:00:00','2026-05-05 09:00:00'),
('job_009','em_003','Phuket Phang Nga Bay James Bond Island Tour','[Phuket Phang Nga Bay James Bond Island Tour]
Driver: Mr. Surasak / 0820009009
Guide: Mr. Thanaphon / 0899010010
Tour Schedule:
07:00-07:30 Hotel pick up
09:00-09:30 Tha Don Pier Departure Phang Nga
09:45-10:45 Koh Panyee Floating Village
11:00-12:00 James Bond Island Photo Stop
12:30-13:30 Lunch on Longtail Boat
13:30-15:00 Sea Canoe into Koh Ping Kan Caves
15:00-16:30 Return Mangrove Cruise
17:30-18:00 Hotel drop off
Including:
- Toyota Commuter VAN transfer
- English Guide
- Longtail boat and sea canoe
- All marine park fees
Not Included:
- Souvenirs at Koh Panyee
Remark:
Full-day sea excursion. Sunscreen recommended.','2026-06-18','2026-06-18','VAN',10,7800.00,'MATCHING',NULL,'2026-04-25 09:00:00','2026-04-25 09:00:00'),
('job_010','em_004','Chiang Rai Hill Tribe & Tea Plantation Tour','[Chiang Rai Hill Tribe & Tea Plantation Tour]
Driver: Mr. Weerasak / 0821010010
Guide: Ms. Chirawan / 0800011011
Tour Schedule:
08:00-08:30 Hotel pick up
09:30-11:00 Choui Fong Tea Plantation
11:00-12:15 Karen Long Neck Village
12:30-13:30 Hill Tribe Lunch
14:00-15:15 Akha Village Handicraft Market
15:30-16:45 Doi Mae Salong Tea Village
17:30-18:30 Mae Fah Luang Art Park
19:00-19:30 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- Tea plantation entrance and tasting
Not Included:
- Handicraft purchases
Remark:
Mountain roads can be winding.','2026-06-25','2026-06-25','VAN',10,5000.00,'SELECTED','fl_009','2026-04-28 10:00:00','2026-05-10 11:00:00'),
('job_011','em_011','Koh Larn Coral Island Snorkeling Day Trip','[Koh Larn Coral Island Snorkeling Day Trip]
Driver: Mr. Adisak / 0822011011
Guide: Ms. Waraporn / 0801012012
Tour Schedule:
08:30-09:00 Hotel pick up
09:30-10:00 Bali Hai Pier Departure
10:30-12:00 Ta Waen Bay Snorkeling
12:00-13:30 Beachside Lunch on Koh Larn
13:30-15:00 Samae Beach Leisure
15:00-15:45 Ferry Return to Pier
16:00-16:30 Hotel drop off
Including:
- Hyundai H1 VAN transfer
- English Guide
- Ferry tickets round trip
- Snorkeling equipment
Not Included:
- Lunch cost
Remark:
Sunscreen strongly advised.','2026-07-03','2026-07-03','VAN',9,3800.00,'MATCHING',NULL,'2026-05-01 09:00:00','2026-05-01 09:00:00'),
('job_012','em_001','Bangkok Grand Palace & Chao Phraya Dinner Cruise','[Bangkok Grand Palace & Chao Phraya Dinner Cruise]
Driver: Mr. Pattanapong / 0823012012
Guide: Ms. Siriporn / 0802013013
Tour Schedule:
08:00-08:30 Hotel pick up
09:00-11:30 Grand Palace & Emerald Buddha Temple
11:30-12:15 Wat Pho Reclining Buddha
12:30-13:30 Riverside Lunch
14:00-15:15 Wat Arun Temple of Dawn
15:30-16:30 Pak Khlong Talad Flower Market
18:00-20:30 Chao Phraya Princess Dinner Cruise
21:00-21:30 Hotel drop off
Including:
- Toyota Commuter VAN
- English & Mandarin Guide
- Grand Palace and temple entrance
- Dinner cruise ticket
Not Included:
- Alcoholic beverages on cruise
Remark:
Modest dress code required at Grand Palace.','2026-07-10','2026-07-10','VAN',10,9500.00,'MATCHING',NULL,'2026-05-05 10:00:00','2026-05-05 10:00:00'),
('job_013','em_003','Phuket Elephant Sanctuary & Waterfall Ethical Tour','[Phuket Elephant Sanctuary & Waterfall Ethical Tour]
Driver: Mr. Boonlert / 0824013013
Guide: Mr. Ekkapon / 0803014014
Tour Schedule:
08:00-08:30 Hotel pick up
09:45-10:00 Elephant Sanctuary Briefing
10:00-11:30 Elephant Feeding & Interaction
12:30-13:30 Vegetarian Lunch at Sanctuary
13:30-14:30 Ton Sai Waterfall & Swimming
15:00-15:45 Bang Pae Waterfall Hike
16:30-17:30 Gibbon Rehabilitation Project
18:00-18:30 Hotel drop off
Including:
- Hyundai H1 VAN transfer
- English Guide
- Elephant sanctuary full experience
- Lunch at sanctuary
Not Included:
- Optional souvenir photos
Remark:
No-riding sanctuary. Conservation focus.','2026-07-15','2026-07-15','VAN',9,6500.00,'SELECTED','fl_003','2026-05-08 11:00:00','2026-05-22 09:00:00'),
('job_014','em_001','Bangkok Floating Market & Damnoen Saduak Tour','[Bangkok Floating Market & Damnoen Saduak Tour]
Driver: Mr. Chaiwat / 0825014014
Guide: Ms. Nanthawan / 0804015015
Tour Schedule:
07:00-07:30 Hotel pick up
08:30-10:30 Damnoen Saduak Floating Market
11:00-12:30 Rose Garden Cultural Show
12:30-13:30 Lunch at Garden Restaurant
14:30-16:00 Maeklong Railway Market
16:30-18:00 Amphawa Floating Market
19:30-20:00 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- Cultural show entrance
Not Included:
- Lunch cost
Remark:
Traffic on the return may vary.','2026-07-20','2026-07-20','VAN',10,6000.00,'OPEN',NULL,'2026-05-10 09:00:00','2026-05-10 09:00:00'),
('job_015','em_015','Krabi Railay Beach & Rock Climbing Adventure','[Krabi Railay Beach & Rock Climbing Adventure]
Driver: Mr. Nathakorn / 0826015015
Guide: Mr. Supakit / 0805016016
Tour Schedule:
08:00-08:30 Hotel pick up
08:45-09:15 Longtail Boat to Railay Beach West
09:30-10:45 Railay East Lagoon Trail
11:00-12:45 Rock Climbing Introduction Session
13:00-14:00 Picnic Lunch at Railay Beach
14:00-14:45 Phra Nang Cave & Princess Cave
15:00-16:15 Free Swim at Phra Nang Beach
16:30-17:30 Return & Hotel drop off
Including:
- Hyundai H1 VAN transfer
- English Guide
- Longtail boat round trip
- Climbing equipment and instructor
Not Included:
- Additional climbing sessions
Remark:
Suitable for beginners. Closed-toe shoes recommended.','2026-07-28','2026-07-28','VAN',9,5600.00,'OPEN',NULL,'2026-05-12 10:00:00','2026-05-12 10:00:00'),
('job_016','em_002','Chiang Mai Cooking Class & Temple Morning Tour','[Chiang Mai Cooking Class & Temple Morning Tour]
Driver: Mr. Anan / 0813002002
Guide: Ms. Ploy / 0893004004
Tour Schedule:
07:30-08:00 Hotel pick up
08:30-10:00 Doi Suthep Temple
10:30-11:00 Thai Cooking School Market Visit
11:00-13:30 Hands-On Thai Cooking Class
14:00-15:30 Chiang Mai Arts & Cultural Centre
16:00-17:00 Warorot Market
17:30-18:00 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- Cooking class ingredients
- Temple entrance
Not Included:
- Personal shopping at Warorot
Remark:
Vegetarian options available on request.','2026-08-05','2026-08-05','VAN',10,4200.00,'OPEN',NULL,'2026-05-20 10:00:00','2026-05-20 10:00:00'),
('job_017','em_004','Chiang Rai Blue Temple & Black House Day Tour','[Chiang Rai Blue Temple & Black House Day Tour]
Driver: Mr. Kitti / 0811223344
Guide: Ms. Oratai / 0895006006
Tour Schedule:
08:30-09:00 Hotel pick up
09:30-10:30 Wat Rong Suea Ten Blue Temple
11:00-12:00 Baan Dam Museum Black House
12:30-13:30 Lunch at Night Bazaar Area
14:00-15:00 Wat Huay Pla Kang Chinese Temple
15:30-16:00 Chiang Rai Clock Tower
16:30-17:00 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- All entrance fees
Not Included:
- Personal expenses
Remark:
Good for half-day or full-day visitors.','2026-08-10','2026-08-10','VAN',10,3800.00,'OPEN',NULL,'2026-05-22 09:00:00','2026-05-22 09:00:00'),
('job_018','em_011','Pattaya Art Museum & Elephant Village Tour','[Pattaya Art Museum & Elephant Village Tour]
Driver: Mr. Withaya / 0819456789
Guide: Ms. Arjuna / 0808901234
Tour Schedule:
09:00-09:30 Hotel pick up
10:00-11:00 Wat Yannasangwararam
11:30-12:30 Pattaya Art Museum
13:00-14:00 Central Festival Pattaya Lunch
14:30-16:00 Pattaya Elephant Village
16:30-17:30 Jomtien Beach Sunset Walk
18:00-18:30 Hotel drop off
Including:
- Hyundai H1 VAN
- English Guide
- Elephant village entrance
Not Included:
- Lunch cost
Remark:
Elephant interaction is observation only at this sanctuary.','2026-08-15','2026-08-15','VAN',9,4000.00,'OPEN',NULL,'2026-05-25 10:00:00','2026-05-25 10:00:00'),
('job_019','em_005','Bangkok Temples Chinatown & Street Food Night Tour','[Bangkok Temples Chinatown & Street Food Night Tour]
Driver: Mr. Chokdi / 0812345699
Guide: Ms. Rattana / 0891234567
Tour Schedule:
09:00-09:30 Hotel pick up
10:00-11:00 Wat Benchamabophit Marble Temple
11:30-12:30 Wat Saket Golden Mount
12:30-13:30 Lunch at Local Restaurant
15:00-17:00 Chinatown Yaowarat Street
17:30-19:30 Street Food Walk Sampeng Lane
20:00-20:30 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- Temple entrance fees
Not Included:
- Street food purchases
Remark:
Wear comfortable walking shoes.','2026-08-20','2026-08-20','VAN',10,4400.00,'OPEN',NULL,'2026-05-28 09:00:00','2026-05-28 09:00:00'),
('job_020','em_007','Bangkok Day Trip to Ayutthaya Historical Park','[Bangkok Day Trip to Ayutthaya Historical Park]
Driver: Mr. Surasak / 0820009009
Guide: Mr. Thanaphon / 0899010010
Tour Schedule:
07:00-07:30 Hotel pick up
09:30-10:30 Wat Phra Si Sanphet
10:30-11:15 Wat Mahathat Buddha in Tree Roots
12:00-13:00 Lunch at Local Ayutthaya Restaurant
13:30-14:30 Wat Chaiwatthanaram
15:00-16:30 Bang Pa-In Royal Palace
18:30-19:00 Hotel drop off
Including:
- Toyota Commuter VAN
- English Guide
- All site entrance fees
Not Included:
- Personal expenses
Remark:
Bring comfortable shoes for ruins walking.','2026-08-25','2026-08-25','VAN',10,5800.00,'OPEN',NULL,'2026-06-01 09:00:00','2026-06-01 09:00:00');


INSERT INTO job_required_languages (job_req_lg_id, job_id, language_name) VALUES
('jrl_001','job_001','English'),('jrl_002','job_001','Mandarin'),
('jrl_003','job_002','English'),
('jrl_004','job_003','English'),
('jrl_005','job_004','English'),('jrl_006','job_004','Mandarin'),
('jrl_007','job_005','English'),
('jrl_008','job_006','English'),('jrl_009','job_006','Thai'),
('jrl_010','job_007','English'),('jrl_011','job_007','Mandarin'),
('jrl_012','job_008','English'),
('jrl_013','job_009','English'),('jrl_014','job_009','Mandarin'),
('jrl_015','job_010','English'),
('jrl_016','job_011','English'),
('jrl_017','job_012','English'),('jrl_018','job_012','Mandarin'),
('jrl_019','job_013','English'),
('jrl_020','job_014','English'),
('jrl_021','job_015','English'),('jrl_022','job_015','Thai'),
('jrl_023','job_016','English'),
('jrl_024','job_017','English'),
('jrl_025','job_018','English'),
('jrl_026','job_019','English'),
('jrl_027','job_020','English');


INSERT INTO job_pickups (job_pickup_id, job_id, pickup_location, pickup_time, sequence) VALUES
('jp_001','job_001','Chiang Mai','07:00-07:30',1),('jp_002','job_001','Chiang Mai','07:30-08:00',2),('jp_003','job_001','Chiang Mai','08:00-08:30',3),
('jp_004','job_002','Phuket','08:00-08:30',1),('jp_005','job_002','Phuket','08:30-09:00',2),('jp_006','job_002','Phuket','09:00-09:30',3),
('jp_007','job_003','Krabi','07:30-08:00',1),('jp_008','job_003','Krabi','08:00-08:30',2),
('jp_009','job_004','Chiang Rai','07:00-07:30',1),('jp_010','job_004','Chiang Rai','07:30-08:00',2),('jp_011','job_004','Chiang Rai','08:00-08:30',3),
('jp_012','job_005','Chonburi','08:00-08:30',1),('jp_013','job_005','Chonburi','08:30-09:00',2),('jp_014','job_005','Chonburi','09:00-09:30',3),
('jp_015','job_006','Chonburi','07:30-08:00',1),('jp_016','job_006','Chonburi','08:00-08:30',2),('jp_017','job_006','Chonburi','08:30-09:00',3),('jp_018','job_006','Chonburi','09:00-09:30',4),
('jp_019','job_007','Chiang Mai','06:30-07:00',1),('jp_020','job_007','Chiang Mai','07:00-07:30',2),('jp_021','job_007','Chiang Mai','07:30-08:00',3),
('jp_022','job_008','Krabi','08:00-08:30',1),('jp_023','job_008','Krabi','08:30-09:00',2),
('jp_024','job_009','Phuket','07:00-07:30',1),('jp_025','job_009','Phuket','07:30-08:00',2),('jp_026','job_009','Phuket','08:00-08:30',3),
('jp_027','job_010','Chiang Rai','08:00-08:30',1),('jp_028','job_010','Chiang Rai','08:30-09:00',2),('jp_029','job_010','Chiang Rai','09:00-09:30',3),
('jp_030','job_011','Chonburi','08:30-09:00',1),('jp_031','job_011','Chonburi','09:00-09:30',2),('jp_032','job_011','Chonburi','09:30-10:00',3),
('jp_033','job_012','Bangkok','08:00-08:30',1),('jp_034','job_012','Bangkok','08:30-09:00',2),('jp_035','job_012','Bangkok','09:00-09:30',3),
('jp_036','job_013','Phuket','08:00-08:30',1),('jp_037','job_013','Phuket','08:30-09:00',2),('jp_038','job_013','Phuket','09:00-09:30',3),
('jp_039','job_014','Bangkok','07:00-07:30',1),('jp_040','job_014','Bangkok','07:30-08:00',2),('jp_041','job_014','Bangkok','08:00-08:30',3),
('jp_042','job_015','Krabi','08:00-08:30',1),('jp_043','job_015','Krabi','08:30-09:00',2),('jp_044','job_015','Krabi','09:00-09:30',3),
('jp_045','job_016','Chiang Mai','07:30-08:00',1),('jp_046','job_016','Chiang Mai','08:00-08:30',2),
('jp_047','job_017','Chiang Rai','08:30-09:00',1),('jp_048','job_017','Chiang Rai','09:00-09:30',2),
('jp_049','job_018','Chonburi','09:00-09:30',1),('jp_050','job_018','Chonburi','09:30-10:00',2),
('jp_051','job_019','Bangkok','09:00-09:30',1),('jp_052','job_019','Bangkok','09:30-10:00',2),('jp_053','job_019','Bangkok','10:00-10:30',3),
('jp_054','job_020','Bangkok','07:00-07:30',1),('jp_055','job_020','Bangkok','07:30-08:00',2),('jp_056','job_020','Bangkok','08:00-08:30',3);


INSERT INTO job_customers (job_customer_id, job_id, customer_name, note) VALUES
('jc_0001','job_001','James Whitfield','Prefers window seat'),('jc_0002','job_001','Laura Whitfield',NULL),('jc_0003','job_001','Michael Zhang','Vegetarian meal required'),('jc_0004','job_001','Sophie Zhang',NULL),('jc_0005','job_001','Robert Tanaka','Mobility assistance needed'),
('jc_0006','job_002','David Harrison',NULL),('jc_0007','job_002','Emily Harrison','Allergic to shellfish'),('jc_0008','job_002','Wei Chen',NULL),('jc_0009','job_002','Fang Chen',NULL),
('jc_0010','job_003','Andrew Thompson','First-time snorkeler'),('jc_0011','job_003','Jessica Thompson',NULL),('jc_0012','job_003','Patrick O Brien',NULL),
('jc_0013','job_004','Thomas Mueller',NULL),('jc_0014','job_004','Ingrid Mueller','Vegetarian'),('jc_0015','job_004','Li Jing',NULL),('jc_0016','job_004','Li Mei',NULL),
('jc_0017','job_005','Samuel Carter',NULL),('jc_0018','job_005','Claire Carter',NULL),('jc_0019','job_005','Nathan Brooks','Diabetic please note meal'),('jc_0020','job_005','Elena Brooks',NULL),('jc_0021','job_005','Kevin Park',NULL),
('jc_0022','job_006','George Wilson',NULL),('jc_0023','job_006','Amanda Wilson',NULL),('jc_0024','job_006','Brian Lee',NULL),
('jc_0025','job_007','Oliver Scott',NULL),('jc_0026','job_007','Hannah Scott','Afraid of heights'),('jc_0027','job_007','Lucas Nguyen',NULL),('jc_0028','job_007','Mia Nguyen',NULL),
('jc_0029','job_008','Daniel Brown',NULL),('jc_0030','job_008','Rachel Brown',NULL),('jc_0031','job_008','Ethan Foster','Cannot swim skip deep kayak'),
('jc_0032','job_009','William Evans',NULL),('jc_0033','job_009','Natalie Evans',NULL),('jc_0034','job_009','Zhao Lei',NULL),('jc_0035','job_009','Zhao Xia',NULL),
('jc_0036','job_010','Christopher Adams',NULL),('jc_0037','job_010','Isabella Adams','Gluten intolerant'),('jc_0038','job_010','Ryan Campbell',NULL),('jc_0039','job_010','Chloe Campbell',NULL),
('jc_0040','job_011','Justin Martin',NULL),('jc_0041','job_011','Ashley Martin',NULL),('jc_0042','job_011','Dylan Harris',NULL),('jc_0043','job_011','Brittany Harris',NULL),
('jc_0044','job_012','Edward Mitchell',NULL),('jc_0045','job_012','Susan Mitchell','Requires wheelchair access where possible'),('jc_0046','job_012','Chen Wei',NULL),('jc_0047','job_012','Lin Fang',NULL),
('jc_0048','job_013','Matthew Walker',NULL),('jc_0049','job_013','Grace Walker',NULL),('jc_0050','job_013','Jack Robinson',NULL),
('jc_0051','job_014','Benjamin Clarke','Group leader'),('jc_0052','job_014','Victoria Clarke',NULL),('jc_0053','job_014','Marcus Reed',NULL),('jc_0054','job_014','Stephanie Reed',NULL),
('jc_0055','job_015','Liam O Connor',NULL),('jc_0056','job_015','Zara O Connor',NULL),('jc_0057','job_015','Harry Patel','No prior climbing experience'),('jc_0058','job_015','Priya Patel',NULL),
('jc_0059','job_016','Anna Kowalski',NULL),('jc_0060','job_016','Piotr Kowalski',NULL),('jc_0061','job_016','Yuki Yamamoto','Nut allergy'),
('jc_0062','job_017','Carlos Rodriguez',NULL),('jc_0063','job_017','Elena Rodriguez',NULL),('jc_0064','job_017','Pierre Dubois',NULL),
('jc_0065','job_018','Ivan Petrov',NULL),('jc_0066','job_018','Olga Petrova',NULL),('jc_0067','job_018','Ahmed Hassan',NULL),('jc_0068','job_018','Layla Hassan',NULL),
('jc_0069','job_019','Raj Sharma',NULL),('jc_0070','job_019','Anita Sharma',NULL),('jc_0071','job_019','Paulo Silva',NULL),('jc_0072','job_019','Ana Silva',NULL),
('jc_0073','job_020','Kenji Yamamoto',NULL),('jc_0074','job_020','Akiko Yamamoto',NULL),('jc_0075','job_020','Kim Min-jun',NULL),('jc_0076','job_020','Park Ji-yeon',NULL);


INSERT INTO job_customer_pickups (id, job_customer_id, job_pickup_id) VALUES
('jcp_001','jc_0001','jp_001'),('jcp_002','jc_0002','jp_001'),('jcp_003','jc_0003','jp_002'),('jcp_004','jc_0004','jp_002'),('jcp_005','jc_0005','jp_003'),
('jcp_006','jc_0006','jp_004'),('jcp_007','jc_0007','jp_004'),('jcp_008','jc_0008','jp_005'),('jcp_009','jc_0009','jp_005'),
('jcp_010','jc_0010','jp_007'),('jcp_011','jc_0011','jp_007'),('jcp_012','jc_0012','jp_008'),
('jcp_013','jc_0013','jp_009'),('jcp_014','jc_0014','jp_009'),('jcp_015','jc_0015','jp_010'),('jcp_016','jc_0016','jp_010'),
('jcp_017','jc_0017','jp_012'),('jcp_018','jc_0018','jp_012'),('jcp_019','jc_0019','jp_013'),('jcp_020','jc_0020','jp_013'),('jcp_021','jc_0021','jp_014'),
('jcp_022','jc_0022','jp_015'),('jcp_023','jc_0023','jp_015'),('jcp_024','jc_0024','jp_016'),
('jcp_025','jc_0025','jp_019'),('jcp_026','jc_0026','jp_019'),('jcp_027','jc_0027','jp_020'),('jcp_028','jc_0028','jp_020'),
('jcp_029','jc_0029','jp_022'),('jcp_030','jc_0030','jp_022'),('jcp_031','jc_0031','jp_023'),
('jcp_032','jc_0032','jp_024'),('jcp_033','jc_0033','jp_024'),('jcp_034','jc_0034','jp_025'),('jcp_035','jc_0035','jp_025'),
('jcp_036','jc_0036','jp_027'),('jcp_037','jc_0037','jp_027'),('jcp_038','jc_0038','jp_028'),('jcp_039','jc_0039','jp_028'),
('jcp_040','jc_0040','jp_030'),('jcp_041','jc_0041','jp_030'),('jcp_042','jc_0042','jp_031'),('jcp_043','jc_0043','jp_031'),
('jcp_044','jc_0044','jp_033'),('jcp_045','jc_0045','jp_033'),('jcp_046','jc_0046','jp_034'),('jcp_047','jc_0047','jp_034'),
('jcp_048','jc_0048','jp_036'),('jcp_049','jc_0049','jp_036'),('jcp_050','jc_0050','jp_037'),
('jcp_051','jc_0051','jp_039'),('jcp_052','jc_0052','jp_039'),('jcp_053','jc_0053','jp_040'),('jcp_054','jc_0054','jp_040'),
('jcp_055','jc_0055','jp_042'),('jcp_056','jc_0056','jp_042'),('jcp_057','jc_0057','jp_043'),('jcp_058','jc_0058','jp_043'),
('jcp_059','jc_0059','jp_045'),('jcp_060','jc_0060','jp_045'),('jcp_061','jc_0061','jp_046'),
('jcp_062','jc_0062','jp_047'),('jcp_063','jc_0063','jp_047'),('jcp_064','jc_0064','jp_048'),
('jcp_065','jc_0065','jp_049'),('jcp_066','jc_0066','jp_049'),('jcp_067','jc_0067','jp_050'),('jcp_068','jc_0068','jp_050'),
('jcp_069','jc_0069','jp_051'),('jcp_070','jc_0070','jp_051'),('jcp_071','jc_0071','jp_052'),('jcp_072','jc_0072','jp_052'),
('jcp_073','jc_0073','jp_054'),('jcp_074','jc_0074','jp_054'),('jcp_075','jc_0075','jp_055'),('jcp_076','jc_0076','jp_055');


INSERT INTO job_itineraries (job_itinerary_id, job_id, place_name, start_time, end_time, note) VALUES
('ji_001','job_001','Hotel Pick Up Nimman Area','07:00','07:30','Collect guests at 3 stops'),('ji_002','job_001','Doi Suthep Temple','08:30','10:00','Modest dress required'),('ji_003','job_001','Old City Moat & Tha Phae Gate','10:30','12:00',NULL),('ji_004','job_001','Lanna Cuisine Lunch','12:00','13:00','Traditional Northern Thai set lunch'),('ji_005','job_001','Silver Handicraft Workshop San Kamphaeng','13:30','15:00','Live silversmithing demonstration'),('ji_006','job_001','Elephant Nature Park Observation','15:30','17:00','No-riding ethical experience'),('ji_007','job_001','Night Bazaar Drop Off','17:30','18:00',NULL),
('ji_008','job_002','Hotel Pick Up Patong Area','08:00','08:30',NULL),('ji_009','job_002','Wat Chalong Temple','09:30','10:30','Largest temple in Phuket'),('ji_010','job_002','Phuket Big Buddha','10:45','11:45','Panoramic island views'),('ji_011','job_002','Phuket Old Town Walking Tour','12:30','14:00','Sino-Portuguese architecture'),('ji_012','job_002','Promthep Cape Viewpoint','15:30','16:30','Best sunset spot in Phuket'),('ji_013','job_002','Rawai Seafood Market','17:00','17:45','Fresh seafood southern tip'),('ji_014','job_002','Hotel Drop Off','18:30','19:00',NULL),
('ji_015','job_003','Hotel Pick Up Ao Nang','07:30','08:00',NULL),('ji_016','job_003','Departure from Nopparat Thara Pier','08:30','09:00','Speedboat safety briefing'),('ji_017','job_003','Poda Island Snorkeling','09:30','10:45','Rich coral reefs'),('ji_018','job_003','Chicken Island Photo Stop','11:00','11:30','Iconic rock formation'),('ji_019','job_003','Tub Island Beachside Lunch','12:00','13:00','BBQ on sandbar'),('ji_020','job_003','Mor Krabi Cave Exploration','13:30','14:30','Limestone sea cave'),('ji_021','job_003','Princess Cave Pranang','15:00','15:45','Sacred sea shrine'),('ji_022','job_003','Return & Hotel Drop Off','16:30','17:00',NULL),
('ji_023','job_004','Hotel Pick Up Chiang Rai','07:00','07:30',NULL),('ji_024','job_004','Wat Rong Khun White Temple','08:00','09:30','Contemporary Buddhist mosaic temple'),('ji_025','job_004','Baan Dam Museum Black House','10:00','11:00','Unconventional dark arts museum'),('ji_026','job_004','Riverside Lunch','12:00','13:00',NULL),('ji_027','job_004','Golden Triangle & Hall of Opium','13:30','15:00','Historic three-border confluence'),('ji_028','job_004','Doi Tung Royal Villa and Garden','15:30','16:45','Former Princess Mother residence'),('ji_029','job_004','Mae Sai Border Town Shopping','17:30','18:30',NULL),('ji_030','job_004','Hotel Drop Off','19:00','19:30',NULL),
('ji_031','job_005','Hotel Pick Up Pattaya','08:00','08:30',NULL),('ji_032','job_005','Sanctuary of Truth','09:00','10:30','All-wood temple mythological carvings'),('ji_033','job_005','Viewpoint Hill Khao Phra Tamnak','10:45','11:30','Panoramic Pattaya Bay view'),('ji_034','job_005','Lunch Walking Street Area','12:00','13:15',NULL),('ji_035','job_005','Nong Nooch Tropical Garden','13:30','15:15','Extensive botanical gardens'),('ji_036','job_005','Nong Nooch Cultural Show','15:30','16:30','Thai dance and elephant show'),('ji_037','job_005','Pattaya Floating Market','17:00','18:15','Four-region Thai cuisine vendors'),('ji_038','job_005','Hotel Drop Off','18:30','19:00',NULL),
('ji_039','job_006','Hotel Pick Up Si Racha','07:30','08:00',NULL),('ji_040','job_006','Sriracha Tiger Zoo','08:30','10:15','Tigers crocodiles exotic animals'),('ji_041','job_006','Crocodile Show','10:30','11:15','Live wrestling and acrobatics'),('ji_042','job_006','Ko Loi Seafood Lunch','12:00','13:15','Seaside causeway restaurant'),('ji_043','job_006','Bang Saen Beach Leisure','14:30','16:15','Family beach with casuarina shade'),('ji_044','job_006','Wat Saman Rattanaram Giant Ganesh','16:30','17:45','Iconic giant pink Ganesh'),('ji_045','job_006','Hotel Drop Off','18:30','19:00',NULL),
('ji_046','job_007','Hotel Pick Up Chiang Mai','06:30','07:00','Early departure three stops'),('ji_047','job_007','Wachirathan Waterfall','08:30','09:30','Second largest on Doi Inthanon'),('ji_048','job_007','Twin Royal Pagodas','10:00','11:00','Built to honor the King and Queen'),('ji_049','job_007','Summit of Doi Inthanon','11:30','12:15','Highest point in Thailand 2565 m'),('ji_050','job_007','Lunch Royal Agricultural Research Center','13:00','14:00','Fresh highland vegetables'),('ji_051','job_007','Sirithan Waterfall','14:30','15:15','Viewable from roadside platform'),('ji_052','job_007','Karen Hill Tribe Village','16:00','17:15','Traditional handicrafts'),('ji_053','job_007','Hotel Drop Off','18:00','18:30',NULL),
('ji_054','job_008','Hotel Pick Up Krabi Town','08:00','08:30',NULL),('ji_055','job_008','Ao Thalane Kayak Briefing','09:00','09:30','Equipment and safety'),('ji_056','job_008','Mangrove Forest Kayaking','09:30','11:30','Limestone tunnels and waterways'),('ji_057','job_008','Bat Cave Sea Cave','11:30','12:15','Cave with thousands of bats'),('ji_058','job_008','Sandbar Picnic Lunch','12:30','13:30','Beachside at low tide'),('ji_059','job_008','Lagoon Return Paddle','14:00','15:15','Open lagoon route'),('ji_060','job_008','Tiger Cave Temple Climb','15:30','17:30','1237 steps panoramic summit'),('ji_061','job_008','Hotel Drop Off','18:30','19:00',NULL),
('ji_062','job_009','Hotel Pick Up Phuket','07:00','07:30',NULL),('ji_063','job_009','Tha Don Pier Departure','09:00','09:30','Board longtail boat'),('ji_064','job_009','Koh Panyee Floating Village','09:45','10:45','Village on stilts over water'),('ji_065','job_009','James Bond Island Koh Tapu','11:00','12:00','Iconic limestone pillar'),('ji_066','job_009','Lunch on Longtail Boat','12:30','13:30',NULL),('ji_067','job_009','Sea Canoe Koh Ping Kan Caves','13:30','15:00','Hidden lagoons and cave systems'),('ji_068','job_009','Return Mangrove Cruise','15:00','16:30',NULL),('ji_069','job_009','Hotel Drop Off','17:30','18:00',NULL),
('ji_070','job_010','Hotel Pick Up Chiang Rai','08:00','08:30',NULL),('ji_071','job_010','Choui Fong Tea Plantation','09:30','11:00','Oolong and green tea tasting'),('ji_072','job_010','Karen Long Neck Village','11:00','12:15','Kayan Lahwi traditional village'),('ji_073','job_010','Hill Tribe Lunch','12:30','13:30',NULL),('ji_074','job_010','Akha Village Handicraft Market','14:00','15:15','Textiles and jewelry'),('ji_075','job_010','Doi Mae Salong Chinese Tea Village','15:30','16:45','Yunnan Chinese settlers tea'),('ji_076','job_010','Mae Fah Luang Art Park','17:30','18:30','Lanna Buddhist art collection'),('ji_077','job_010','Hotel Drop Off','19:00','19:30',NULL),
('ji_078','job_011','Hotel Pick Up Jomtien','08:30','09:00',NULL),('ji_079','job_011','Bali Hai Pier Departure','09:30','10:00',NULL),('ji_080','job_011','Ta Waen Bay Snorkeling','10:30','12:00','Coral reefs tropical fish'),('ji_081','job_011','Beachside Lunch Koh Larn','12:00','13:30',NULL),('ji_082','job_011','Samae Beach Leisure','13:30','15:00','Swimming sunbathing watersports'),('ji_083','job_011','Ferry Return to Pier','15:00','15:45',NULL),('ji_084','job_011','Hotel Drop Off','16:00','16:30',NULL),
('ji_085','job_012','Hotel Pick Up Sukhumvit','08:00','08:30',NULL),('ji_086','job_012','Grand Palace & Emerald Buddha','09:00','11:30','Dress code strictly enforced'),('ji_087','job_012','Wat Pho Reclining Buddha','11:30','12:15','46 metre gold reclining Buddha'),('ji_088','job_012','Riverside Lunch','12:30','13:30',NULL),('ji_089','job_012','Wat Arun Temple of Dawn','14:00','15:15','Porcelain prang tower'),('ji_090','job_012','Pak Khlong Talad Flower Market','15:30','16:30',NULL),('ji_091','job_012','Chao Phraya Dinner Cruise','18:00','20:30','Buffet dinner illuminated landmarks'),('ji_092','job_012','Hotel Drop Off','21:00','21:30',NULL),
('ji_093','job_013','Hotel Pick Up Rawai','08:00','08:30',NULL),('ji_094','job_013','Elephant Sanctuary Briefing','09:45','10:00','Rules and behavior'),('ji_095','job_013','Elephant Feeding & Interaction','10:00','11:30','Fruit feeding jungle walk'),('ji_096','job_013','Vegetarian Lunch at Sanctuary','12:30','13:30','Organic kitchen'),('ji_097','job_013','Ton Sai Waterfall & Swimming','13:30','14:30','Natural pool beneath fall'),('ji_098','job_013','Bang Pae Waterfall Hike','15:00','15:45','Largest waterfall in Phuket'),('ji_099','job_013','Gibbon Rehabilitation Project','16:30','17:30','Observe gibbons for release'),('ji_100','job_013','Hotel Drop Off','18:00','18:30',NULL),
('ji_101','job_014','Hotel Pick Up Bangkok','07:00','07:30',NULL),('ji_102','job_014','Damnoen Saduak Floating Market','08:30','10:30','Paddle through market canals'),('ji_103','job_014','Rose Garden Cultural Show','11:00','12:30','Traditional dances and ceremonies'),('ji_104','job_014','Lunch at Garden Restaurant','12:30','13:30',NULL),('ji_105','job_014','Maeklong Railway Market','14:30','16:00','Market on active train tracks'),('ji_106','job_014','Amphawa Floating Market','16:30','18:00','Evening riverside market'),('ji_107','job_014','Hotel Drop Off','19:30','20:00',NULL),
('ji_108','job_015','Hotel Pick Up Ao Nang','08:00','08:30',NULL),('ji_109','job_015','Longtail Boat to Railay Beach West','08:45','09:15',NULL),('ji_110','job_015','Railay East Lagoon Trail','09:30','10:45','Jungle trail emerald lagoon'),('ji_111','job_015','Rock Climbing Introduction','11:00','12:45','Beginner limestone wall certified instructor'),('ji_112','job_015','Picnic Lunch Railay Beach','13:00','14:00',NULL),('ji_113','job_015','Phra Nang Cave & Princess Cave','14:00','14:45','Sacred sea spirit shrine'),('ji_114','job_015','Free Swim Phra Nang Beach','15:00','16:15','Most beautiful beach in Krabi'),('ji_115','job_015','Return & Hotel Drop Off','16:30','17:30',NULL),
('ji_116','job_016','Hotel Pick Up Chiang Mai','07:30','08:00',NULL),('ji_117','job_016','Doi Suthep Temple','08:30','10:00',NULL),('ji_118','job_016','Thai Cooking School Market Visit','10:30','11:00',NULL),('ji_119','job_016','Hands-On Thai Cooking Class','11:00','13:30','Prepare 4 authentic dishes'),('ji_120','job_016','Chiang Mai Arts & Cultural Centre','14:00','15:30',NULL),('ji_121','job_016','Warorot Market','16:00','17:00',NULL),('ji_122','job_016','Hotel Drop Off','17:30','18:00',NULL),
('ji_123','job_017','Hotel Pick Up Chiang Rai','08:30','09:00',NULL),('ji_124','job_017','Wat Rong Suea Ten Blue Temple','09:30','10:30','Vivid blue murals interior'),('ji_125','job_017','Baan Dam Museum Black House','11:00','12:00',NULL),('ji_126','job_017','Lunch Night Bazaar Area','12:30','13:30',NULL),('ji_127','job_017','Wat Huay Pla Kang Chinese Temple','14:00','15:00','18-storey Chinese Guanyin statue'),('ji_128','job_017','Chiang Rai Clock Tower','15:30','16:00','Light show at dusk'),('ji_129','job_017','Hotel Drop Off','16:30','17:00',NULL),
('ji_130','job_018','Hotel Pick Up Pattaya','09:00','09:30',NULL),('ji_131','job_018','Wat Yannasangwararam','10:00','11:00','Important regional temple'),('ji_132','job_018','Pattaya Art Museum','11:30','12:30','3D interactive art installation'),('ji_133','job_018','Central Festival Pattaya Lunch','13:00','14:00',NULL),('ji_134','job_018','Pattaya Elephant Village','14:30','16:00','Observation and feeding'),('ji_135','job_018','Jomtien Beach Sunset Walk','16:30','17:30',NULL),('ji_136','job_018','Hotel Drop Off','18:00','18:30',NULL),
('ji_137','job_019','Hotel Pick Up Bangkok','09:00','09:30',NULL),('ji_138','job_019','Wat Benchamabophit Marble Temple','10:00','11:00','European marble royal temple'),('ji_139','job_019','Wat Saket Golden Mount','11:30','12:30','Panoramic Bangkok city view'),('ji_140','job_019','Lunch Local Bangkok Restaurant','12:30','13:30',NULL),('ji_141','job_019','Chinatown Yaowarat Street','15:00','17:00','Gold shops street food'),('ji_142','job_019','Street Food Walk Sampeng Lane','17:30','19:30','Historic textile trading lane'),('ji_143','job_019','Hotel Drop Off','20:00','20:30',NULL),
('ji_144','job_020','Hotel Pick Up Bangkok','07:00','07:30',NULL),('ji_145','job_020','Wat Phra Si Sanphet','09:30','10:30','Three chedis royal chapel ruins'),('ji_146','job_020','Wat Mahathat Buddha in Tree Roots','10:30','11:15','Famous sandstone Buddha head'),('ji_147','job_020','Lunch Local Ayutthaya Restaurant','12:00','13:00',NULL),('ji_148','job_020','Wat Chaiwatthanaram','13:30','14:30','Riverside Khmer-style temple'),('ji_149','job_020','Bang Pa-In Royal Palace','15:00','16:30','Mixed Thai and European architecture'),('ji_150','job_020','Hotel Drop Off','18:30','19:00',NULL);


INSERT INTO job_applications (job_application_id, job_id, fl_id, application_status, applied_at, selected_at) VALUES
('ja_001','job_001','fl_001','ACCEPTED','2026-04-03 10:00:00','2026-04-08 14:00:00'),
('ja_002','job_001','fl_009','REJECTED','2026-04-04 09:00:00',NULL),
('ja_003','job_001','fl_032','REJECTED','2026-04-05 11:00:00',NULL),
('ja_004','job_002','fl_003','ACCEPTED','2026-04-07 09:00:00','2026-04-12 10:00:00'),
('ja_005','job_002','fl_024','REJECTED','2026-04-08 10:00:00',NULL),
('ja_006','job_002','fl_048','REJECTED','2026-04-09 13:00:00',NULL),
('ja_007','job_003','fl_016','ACCEPTED','2026-04-10 09:00:00','2026-04-20 14:00:00'),
('ja_008','job_003','fl_036','REJECTED','2026-04-11 11:00:00',NULL),
('ja_009','job_003','fl_019','REJECTED','2026-04-12 10:00:00',NULL),
('ja_010','job_004','fl_045','ACCEPTED','2026-04-12 08:00:00','2026-04-18 13:00:00'),
('ja_011','job_004','fl_009','REJECTED','2026-04-13 10:00:00',NULL),
('ja_012','job_004','fl_034','REJECTED','2026-04-14 09:00:00',NULL),
('ja_013','job_005','fl_017','ACCEPTED','2026-04-16 10:00:00','2026-04-22 09:00:00'),
('ja_014','job_005','fl_033','REJECTED','2026-04-17 11:00:00',NULL),
('ja_015','job_005','fl_046','REJECTED','2026-04-18 09:30:00',NULL),
('ja_016','job_006','fl_028','ACCEPTED','2026-04-20 10:00:00','2026-04-26 09:00:00'),
('ja_017','job_006','fl_017','REJECTED','2026-04-21 09:00:00',NULL),
('ja_018','job_006','fl_033','REJECTED','2026-04-22 11:00:00',NULL),
('ja_019','job_007','fl_001','ACCEPTED','2026-04-22 09:00:00','2026-05-02 13:00:00'),
('ja_020','job_007','fl_010','REJECTED','2026-04-23 10:00:00',NULL),
('ja_021','job_007','fl_050','REJECTED','2026-04-24 11:00:00',NULL),
('ja_022','job_008','fl_036','ACCEPTED','2026-04-23 09:30:00','2026-05-05 09:00:00'),
('ja_023','job_008','fl_016','REJECTED','2026-04-24 10:00:00',NULL),
('ja_024','job_008','fl_003','REJECTED','2026-04-25 11:00:00',NULL),
('ja_025','job_009','fl_003','APPLIED','2026-04-26 09:00:00',NULL),
('ja_026','job_009','fl_024','APPLIED','2026-04-27 10:30:00',NULL),
('ja_027','job_009','fl_011','APPLIED','2026-04-28 11:00:00',NULL),
('ja_028','job_010','fl_009','ACCEPTED','2026-04-30 09:00:00','2026-05-10 11:00:00'),
('ja_029','job_010','fl_045','REJECTED','2026-05-01 10:00:00',NULL),
('ja_030','job_010','fl_004','REJECTED','2026-05-02 11:00:00',NULL),
('ja_031','job_011','fl_017','APPLIED','2026-05-02 09:00:00',NULL),
('ja_032','job_011','fl_033','APPLIED','2026-05-03 10:00:00',NULL),
('ja_033','job_011','fl_046','APPLIED','2026-05-04 11:00:00',NULL),
('ja_034','job_012','fl_019','APPLIED','2026-05-06 09:00:00',NULL),
('ja_035','job_012','fl_023','APPLIED','2026-05-07 10:00:00',NULL),
('ja_036','job_012','fl_011','APPLIED','2026-05-08 11:30:00',NULL),
('ja_037','job_013','fl_003','ACCEPTED','2026-05-09 09:00:00','2026-05-22 09:00:00'),
('ja_038','job_013','fl_024','REJECTED','2026-05-10 11:00:00',NULL),
('ja_039','job_013','fl_048','REJECTED','2026-05-11 10:00:00',NULL),
('ja_040','job_014','fl_019','APPLIED','2026-05-11 09:00:00',NULL),
('ja_041','job_014','fl_023','APPLIED','2026-05-12 10:00:00',NULL),
('ja_042','job_015','fl_016','APPLIED','2026-05-13 09:00:00',NULL),
('ja_043','job_015','fl_036','APPLIED','2026-05-14 10:00:00',NULL),
('ja_044','job_015','fl_008','APPLIED','2026-05-15 11:00:00',NULL),
('ja_045','job_016','fl_001','APPLIED','2026-05-21 09:00:00',NULL),
('ja_046','job_016','fl_010','APPLIED','2026-05-22 10:00:00',NULL),
('ja_047','job_017','fl_009','APPLIED','2026-05-23 09:00:00',NULL),
('ja_048','job_017','fl_045','APPLIED','2026-05-24 10:00:00',NULL),
('ja_049','job_018','fl_017','APPLIED','2026-05-26 09:00:00',NULL),
('ja_050','job_018','fl_028','APPLIED','2026-05-27 10:00:00',NULL),
('ja_051','job_018','fl_046','APPLIED','2026-05-28 11:00:00',NULL),
('ja_052','job_019','fl_011','APPLIED','2026-05-29 09:00:00',NULL),
('ja_053','job_019','fl_019','APPLIED','2026-05-30 10:00:00',NULL),
('ja_054','job_020','fl_002','APPLIED','2026-06-02 09:00:00',NULL),
('ja_055','job_020','fl_005','APPLIED','2026-06-03 10:00:00',NULL),
('ja_056','job_020','fl_011','APPLIED','2026-06-04 11:00:00',NULL);


INSERT INTO job_payments (payment_id, job_id, em_id, fl_id, payment_status, slip_url, reject_reason, paid_at, confirmed_at) VALUES
('pay_001','job_001','em_002','fl_001','CONFIRMED','https://example.com/slips/pay_001.jpg',NULL,'2026-04-10 10:00:00','2026-04-11 09:00:00'),
('pay_002','job_002','em_003','fl_003','CONFIRMED','https://example.com/slips/pay_002.jpg',NULL,'2026-04-14 11:00:00','2026-04-15 10:00:00'),
('pay_003','job_003','em_015','fl_016','CONFIRMED','https://example.com/slips/pay_003.jpg',NULL,'2026-04-22 10:00:00','2026-04-23 09:00:00'),
('pay_004','job_004','em_004','fl_045','CONFIRMED','https://example.com/slips/pay_004.jpg',NULL,'2026-04-20 09:00:00','2026-04-21 10:00:00'),
('pay_005','job_005','em_011','fl_017','CONFIRMED','https://example.com/slips/pay_005.jpg',NULL,'2026-04-24 10:00:00','2026-04-25 09:00:00'),
('pay_006','job_006','em_019','fl_028','REJECTED','https://example.com/slips/pay_006_v1.jpg','Slip image is blurry and amount is unreadable. Please resubmit a clear photo.','2026-04-28 09:00:00',NULL),
('pay_007','job_006','em_019','fl_028','CONFIRMED','https://example.com/slips/pay_006_v2.jpg',NULL,'2026-04-30 10:00:00','2026-05-01 09:00:00'),
('pay_008','job_007','em_002','fl_001','PAID','https://example.com/slips/pay_008.jpg',NULL,'2026-05-04 10:00:00',NULL),
('pay_009','job_008','em_015','fl_036','PENDING','https://example.com/slips/pay_009.jpg',NULL,NULL,NULL),
('pay_010','job_010','em_004','fl_009','PAID','https://example.com/slips/pay_010.jpg',NULL,'2026-05-12 10:00:00',NULL),
('pay_011','job_013','em_003','fl_003','PENDING','https://example.com/slips/pay_011.jpg',NULL,NULL,NULL);


INSERT INTO fl_reviews (fl_review_id, job_id, em_id, fl_id, rating, comment, reviewed_at) VALUES
('flr_001','job_001','em_002','fl_001',5,'Excellent driver, very punctual and professional. Guests were extremely happy with the service.','2026-05-12 09:00:00'),
('flr_002','job_002','em_003','fl_003',5,'Great service! The driver communicated well and helped guests throughout the entire tour.','2026-05-17 10:00:00'),
('flr_003','job_003','em_015','fl_016',4,'Very smooth ride. The van was clean and comfortable. Highly recommended for island tours.','2026-05-22 09:00:00'),
('flr_004','job_004','em_004','fl_045',5,'Driver was knowledgeable about local attractions and spoke excellent English throughout.','2026-05-25 10:00:00'),
('flr_005','job_005','em_011','fl_017',4,'Outstanding performance. Will definitely hire this driver again for future Pattaya tours.','2026-06-03 09:00:00'),
('flr_006','job_006','em_019','fl_028',4,'Reliable and friendly driver. The tour went exactly as planned despite heavy traffic.','2026-06-07 10:00:00');


INSERT INTO em_reviews (em_review_id, job_id, fl_id, em_id, rating, comment, reviewed_at) VALUES
('emr_001','job_001','fl_001','em_002',5,'Great employer to work with. Clear instructions and timely payment confirmed.','2026-05-12 10:00:00'),
('emr_002','job_002','fl_003','em_003',5,'Job details were well organized. Very professional company throughout the process.','2026-05-17 11:00:00'),
('emr_003','job_003','fl_016','em_015',4,'Payment was confirmed on time. Would happily work with this employer again.','2026-05-22 10:00:00'),
('emr_004','job_004','fl_045','em_004',5,'Clear job briefing and responsive communication throughout the entire tour day.','2026-05-25 11:00:00'),
('emr_005','job_005','fl_017','em_011',4,'Very smooth working experience. Job description was detailed and fully accurate.','2026-06-03 10:00:00'),
('emr_006','job_006','fl_028','em_019',4,'Professional employer with clear expectations. Payment process was straightforward.','2026-06-07 11:00:00');
