create database if not exists qlsv;
use qlsv;
create table if not exists PHONG_BAN (
	PB_ID varchar(10) not null primary key,
    PB_TEN varchar(50) null
);

insert into phong_ban 
(pb_id, pb_ten)
values
('pb001', 'Phong IT'),
('pb002', 'Phong ke toan'),
('pb003', 'Ban giam doc');

create table if not exists NHAN_VIEN(
	NV_ID varchar(10) not null primary key,
    NV_GioiTinh varchar(3) null,
    NV_Ten varchar(50) null,
    NV_NSinh date null,
    NV_SDT varchar(10) null,
    NV_PhongBan varchar(10) null,
    NV_MatKhau varchar(12) null,
    NV_NGAYPHEPCONLAI int null,
    NV_LUONGTHEOGIO double null,
    
    constraint fk_NV_PB foreign key(NV_PhongBan) references PHONG_BAN(PB_ID)
);

insert into nhan_vien
(NV_ID, NV_GioiTinh, NV_Ten, NV_NSinh, NV_SDT, NV_PhongBan, NV_MatKhau, NV_NGAYPHEPCONLAI, NV_LUONGTHEOGIO)
values
('nv001', 'Nam', 'Nguyen Van A', '2000-01-01', '0123456789', 'pb001', 'NhanVien01', 12, 30000),
('nv002', 'Nu', 'Nguyen Thi B', '2000-01-01', '0123456788', 'pb002', 'NhanVien02', 12, 40000),
('nv003', 'Nam', 'Nguyen Van C', '2000-01-01', '0123456787', 'pb003', 'NhanVien03', 12, 50000),
('nv004', 'Nu', 'Nguyen Thi D', '2000-01-01', '0123456786', 'pb001', 'NhanVien04', 12, 30000),
('nv005', 'Nam', 'Nguyen Van E', '2000-01-01', '0123456785', 'pb002', 'NhanVien05', 12, 40000),
('nv006', 'Nu', 'Nguyen Thi F', '2000-01-01', '0123456784', 'pb003', 'NhanVien06', 12, 50000),
('nv007', 'Nam', 'Nguyen Van G', '2000-01-01', '0123456783', 'pb001', 'NhanVien07', 12, 30000),
('nv008', 'Nu', 'Nguyen Thi H', '2000-01-01', '0123456782', 'pb002', 'NhanVien08', 12, 40000),
('nv009', 'Nam', 'Nguyen Van I', '2000-01-01', '0123456781', 'pb003', 'NhanVien09', 12, 50000),
('nv010', 'Nu', 'Nguyen Thi K', '2000-01-01', '0123456780', 'pb001', 'NhanVien10', 12, 30000),
('nv011', 'Nam', 'Nguyen Van L', '2000-01-01', '0123456799', 'pb002', 'NhanVien11', 12, 40000),
('nv012', 'Nu', 'Nguyen Thi M', '2000-01-01', '0123456709', 'pb003', 'NhanVien012', 12, 50000),
('nv013', 'Nam', 'Nguyen Van N', '2000-01-01', '0123456779', 'pb001', 'NhanVien13', 12, 30000),
('nv014', 'Nu', 'Nguyen Thi O', '2000-01-01', '0123456769', 'pb002', 'NhanVien14', 12, 40000),
('nv015', 'Nam', 'Nguyen Van P', '2000-01-01', '0123456759', 'pb003', 'NhanVien15', 12, 50000),
('nv016', 'Nu', 'Nguyen Thi Q', '2000-01-01', '0123456749', 'pb001', 'NhanVien16', 12, 30000),
('nv017', 'Nam', 'Nguyen Van R', '2000-01-01', '0123456739', 'pb002', 'NhanVien17', 12, 40000),
('nv018', 'Nu', 'Nguyen Thi S', '2000-01-01', '0123456729', 'pb003', 'NhanVien18', 12, 50000),
('nv019', 'Nam', 'Nguyen Van T', '2000-01-01', '0123456719', 'pb001', 'NhanVien19', 12, 30000),
('nv020', 'Nu', 'Nguyen Thi U', '2000-01-01', '0123456979', 'pb002', 'NhanVien20', 12, 40000);

create table if not exists QUAN_LI(
	ID_QLI varchar(10) not null,
    ID_NV varchar(10) not null,
    
    constraint fk_ql_nv foreign key (ID_QLI) references NHAN_VIEN(NV_ID),
    constraint fk_nv_nv foreign key (ID_NV) references NHAN_VIEN(NV_ID)
);
insert into quan_li
(ID_QLI, ID_NV)
values
('nv001', 'nv004'),
('nv001', 'nv007'),
('nv004', 'nv010'),
('nv004', 'nv013'),
('nv007', 'nv016'),
('nv007', 'nv019'),

('nv002', 'nv005'),
('nv002', 'nv008'),
('nv005', 'nv011'),
('nv005', 'nv014'),
('nv008', 'nv017'),
('nv007', 'nv020'),

('nv003', 'nv006'),
('nv006', 'nv009'),
('nv006', 'nv012'),
('nv006', 'nv015'),
('nv006', 'nv018')




