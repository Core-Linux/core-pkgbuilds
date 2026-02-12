# Maintainer: EosOS GNU/linux <eososlinux@gmail.com>

pkgname=core-skel-kde
pkgver=1.0
pkgrel=1
pkgdesc="Core skel configuration for KDE Plasma live session"
arch=('any')
url="https://github.com/sourcecorearch/core-skel-kde"
license=('GPL3')
depends=('plasma-workspace')
source=("git+https://github.com/sourcecorearch/core-skel-kde.git")
sha256sums=('SKIP')

package() {
  cp -r "${srcdir}/${pkgname}/src/etc/skel/"* "${pkgdir}/etc/skel/"
}
